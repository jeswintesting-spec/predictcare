from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, F, Q
from datetime import date, timedelta
import pandas as pd
import json
from django.db.models.functions import TruncDate
from .models import Medicine, PrescriptionLine, PharmacyBill, BillItem
from hospital.models import Visit, Patient
from ml.predict_load import predict_medicine_demand_from_df

def inventory_list(request):
    """Displays the current medicine inventory with pagination."""
    query = request.GET.get('q')
    if query:
        medicines_list = Medicine.objects.filter(name__icontains=query).order_by('name')
    else:
        medicines_list = Medicine.objects.all().order_by('name')
        
    from django.core.paginator import Paginator
    paginator = Paginator(medicines_list, 50) # 50 per page
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)
    
    return render(request, 'pharmacy/inventory_list.html', {'medicines': medicines, 'query': query})

def bill_history(request):
    """View to show history of all bills with optimized search and pagination."""
    from .models import PharmacyBill
    from django.core.paginator import Paginator
    from django.db.models import Count, Q
    
    query = request.GET.get('q')
    if query:
        # Search by Invoice ID or Customer Name
        lookup = Q(customer_name__icontains=query)
        if query.isdigit():
            lookup |= Q(id=int(query))
            
        bills_list = PharmacyBill.objects.filter(lookup).select_related('patient').annotate(item_count=Count('items')).order_by('-created_at')
    else:
        bills_list = PharmacyBill.objects.all().select_related('patient').annotate(item_count=Count('items')).order_by('-created_at')
    
    paginator = Paginator(bills_list, 50) # Show 50 per page
    page_number = request.GET.get('page')
    bills = paginator.get_page(page_number)
    
    return render(request, 'pharmacy/bill_history.html', {
        'bills': bills,
        'query': query,
        'total_count': bills_list.count()
    })

def billing_view(request):
    """
    Search for patient and show billable medicines from recent visits.
    """
    patient = None
    visits = []
    billable_items = []
    total_amount = 0.0
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            from django.db import transaction
            try:
                with transaction.atomic():
                    patient = Patient.objects.get(patient_id=patient_id)
                    visits = Visit.objects.filter(patient=patient, visit_date=date.today())
                    prescriptions = PrescriptionLine.objects.filter(visit__in=visits).select_related('medicine')
                    
                    if not prescriptions.exists():
                        # Check for legacy medicines if no PrescriptionLines
                        old_visits = visits.filter(prescriptions__isnull=True).exclude(medicines="")
                        if not old_visits.exists():
                            messages.error(request, "No billable medicines found for this patient today.")
                            return redirect('pharmacy_billing')
                    
                    # Collect tax and discount percentages
                    tax_pc = float(request.POST.get('tax_percentage', 0) or 0)
                    discount_pc = float(request.POST.get('discount_percentage', 0) or 0)

                    # Create the bill with initial breakdown
                    bill = PharmacyBill.objects.create(
                        customer_name=patient.patient_name,
                        patient=patient,
                        subtotal=0,
                        tax_percentage=tax_pc,
                        discount_percentage=discount_pc,
                        total_amount=0
                    )
                    
                    calc_subtotal = 0
                    # Handle proper prescriptions
                    for p in prescriptions:
                        med = p.medicine
                        qty = p.quantity
                        item_total = float(med.price) * qty
                        
                        if med.stock_quantity >= qty:
                            med.stock_quantity -= qty
                            med.save()
                        
                        BillItem.objects.create(
                            bill=bill,
                            medicine=med,
                            quantity=qty,
                            price_per_unit=med.price,
                            total_price=item_total
                        )
                        calc_subtotal += item_total
                    
                    # Handle legacy medicines (if any)
                    old_visits = visits.filter(prescriptions__isnull=True).exclude(medicines="")
                    import re
                    for v in old_visits:
                        med_names = [m.strip() for m in v.medicines.split(',') if m.strip()]
                        for m_name in med_names:
                            qty = 1
                            name = m_name
                            
                            dos_match = re.search(r'\((.*?)\)', name)
                            if dos_match: name = name.replace(dos_match.group(0), '')
                            qty_matches = re.findall(r'[x×X](\d+)', name)
                            if qty_matches:
                                qty = int(qty_matches[-1])
                                name = re.sub(r'[x×X]\d+', '', name)
                            name = name.strip()
                            
                            try:
                                med_obj = Medicine.objects.get(name__iexact=name)
                                item_total = float(med_obj.price) * qty
                                if med_obj.stock_quantity >= qty:
                                    med_obj.stock_quantity -= qty
                                    med_obj.save()
                                
                                BillItem.objects.create(
                                    bill=bill,
                                    medicine=med_obj,
                                    quantity=qty,
                                    price_per_unit=med_obj.price,
                                    total_price=item_total
                                )
                                calc_subtotal += item_total
                            except Medicine.DoesNotExist:
                                continue

                    # Final Calculations
                    tax_amt = (calc_subtotal * tax_pc) / 100
                    discount_amt = (calc_subtotal * discount_pc) / 100
                    final_total = calc_subtotal + tax_amt - discount_amt

                    bill.subtotal = calc_subtotal
                    bill.tax_amount = tax_amt
                    bill.discount_amount = discount_amt
                    bill.total_amount = final_total
                    bill.save()
                    
                    messages.success(request, f"Bill #{bill.id} generated successfully for {patient.patient_name}! Total: ₹{calc_total}")
                    return redirect('bill_history')
            except Patient.DoesNotExist:
                messages.error(request, "Patient not found.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        return redirect('pharmacy_billing')

    query = request.GET.get('q')
    if query:
        # Search by ID or Name
        patients = Patient.objects.filter(
            Q(patient_id__iexact=query) | 
            Q(patient_name__icontains=query)
        )
        if patients.exists():
            patient = patients.first() # Take the first match for now
            
            # Get recent visits (Today only for now, or last 24h)
            visits = Visit.objects.filter(patient=patient, visit_date=date.today())
            
            # Collect medicines using proper PrescriptionLine objects
            prescriptions = PrescriptionLine.objects.filter(visit__in=visits).select_related('medicine')
            
            for p in prescriptions:
                med_obj = p.medicine
                qty = p.quantity
                item_total = float(med_obj.price) * qty
                
                billable_items.append({
                    'visit_id': p.visit.id,
                    'name': f"{med_obj.name} (Qty: {qty})",
                    'price': med_obj.price,
                    'qty': qty,
                    'stock': med_obj.stock_quantity,
                    'available': med_obj.stock_quantity >= qty,
                    'obj': med_obj
                })
                total_amount += item_total
                
        # Fallback for older visits that might still use text field (if migrating)
        # Find visits without prescriptions but with text medicines
        old_visits = visits.filter(prescriptions__isnull=True).exclude(medicines="")
        for visit in old_visits:
            med_names = [m.strip() for m in visit.medicines.split(',') if m.strip()]
            for m_name in med_names:
                import re
                qty = 1
                name = m_name
                
                # parse (dosage)
                dos_match = re.search(r'\((.*?)\)', name)
                if dos_match:
                    name = name.replace(dos_match.group(0), '')
                    
                # parse xQty or ×Qty
                qty_matches = re.findall(r'[x×X](\d+)', name)
                if qty_matches:
                    qty = int(qty_matches[-1])  # Take the last mentioned quantity
                    name = re.sub(r'[x×X]\d+', '', name)
                    
                name = name.strip()
                try:
                    med_obj = Medicine.objects.get(name__iexact=name)
                    billable_items.append({
                        'visit_id': visit.id,
                        'name': f"{name} (Qty: {qty}) - Legacy",
                        'price': med_obj.price,
                        'qty': qty,
                        'stock': med_obj.stock_quantity,
                        'available': med_obj.stock_quantity >= qty,
                        'obj': med_obj
                    })
                    total_amount += float(med_obj.price) * qty
                except Medicine.DoesNotExist:
                    billable_items.append({
                        'visit_id': visit.id,
                        'name': name,
                        'price': 0,
                        'qty': qty,
                        'stock': 0,
                        'available': False,
                        'obj': None
                    })

    context = {
        'patient': patient,
        'visits': visits,
        'billable_items': billable_items,
        'total_amount': round(total_amount, 2),
        'query': query
    }
    context = {
        'patient': patient,
        'visits': visits,
        'billable_items': billable_items,
        'total_amount': round(total_amount, 2),
        'query': query
    }
    return render(request, 'pharmacy/billing.html', context)

def manual_billing_view(request):
    """
    Manual billing: Add medicines manually to a cart session.
    """
    if 'cart' not in request.session:
        request.session['cart'] = []

    cart = request.session['cart']
    
    # Calculate totals
    total_amount = sum(float(item['total']) for item in cart)
    
    # Handle Search for Medicines to display info (optional, or just use autocomplete in template)
    # We will pass all medicines for the datalist
    all_medicines = Medicine.objects.all().values('id', 'name', 'price', 'stock_quantity')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            med_name = request.POST.get('medicine_name')
            qty = int(request.POST.get('quantity', 1))
            
            # Find medicine
            try:
                med = Medicine.objects.get(name=med_name)
                # Check if already in cart
                existing = next((item for item in cart if item['id'] == med.id), None)
                if existing:
                    existing['qty'] += qty
                    existing['total'] = float(existing['price']) * existing['qty']
                else:
                    cart.append({
                        'id': med.id,
                        'name': med.name,
                        'price': float(med.price),
                        'qty': qty,
                        'total': float(med.price) * qty
                    })
                request.session.modified = True
                messages.success(request, f"Added {med.name}")
            except Medicine.DoesNotExist:
                messages.error(request, "Medicine not found in inventory.")
                
        elif action == 'remove':
             med_id = int(request.POST.get('med_id'))
             cart = [item for item in cart if item['id'] != med_id]
             request.session['cart'] = cart
             
        elif action == 'clear':
            request.session['cart'] = []
            
        elif action in ['checkout', 'checkout_print']:
            customer_name = request.POST.get('customer_name') or "Walk-in Customer"
            tax_pc = float(request.POST.get('tax_percentage', 0) or 0)
            discount_pc = float(request.POST.get('discount_percentage', 0) or 0)
            
            # Calculate breakdown
            calc_subtotal = float(total_amount)
            tax_amt = (calc_subtotal * tax_pc) / 100
            discount_amt = (calc_subtotal * discount_pc) / 100
            final_total = calc_subtotal + tax_amt - discount_amt

            # Create Bill
            from .models import PharmacyBill, BillItem # Import here to avoid circular
            bill = PharmacyBill.objects.create(
                customer_name=customer_name,
                subtotal=calc_subtotal,
                tax_percentage=tax_pc,
                tax_amount=tax_amt,
                discount_percentage=discount_pc,
                discount_amount=discount_amt,
                total_amount=final_total
            )
            
            # Create Items and Update Stock
            for item in cart:
                try:
                    med = Medicine.objects.get(id=item['id'])
                    # Deduct stock
                    if med.stock_quantity >= item['qty']:
                        med.stock_quantity -= item['qty']
                        med.save()
                    else:
                        # Warning if stock changed during session (optional handling)
                        pass
                        
                    BillItem.objects.create(
                        bill=bill,
                        medicine=med,
                        quantity=item['qty'],
                        price_per_unit=item['price'],
                        total_price=item['total']
                    )
                except Medicine.DoesNotExist:
                    continue
            
            request.session['cart'] = []
            messages.success(request, f"Bill #{bill.id} generated successfully for {customer_name}! Total: ₹{final_total}.")
            if action == 'checkout_print':
                return redirect('print_bill', bill_id=bill.id)
            return redirect('bill_history')
            
        return redirect('manual_billing')

    context = {
        'cart': cart,
        'total_amount': total_amount,
        'all_medicines': all_medicines
    }
    return render(request, 'pharmacy/manual_billing.html', context)


def add_medicine(request):
    """View to add new medicine to inventory."""
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        min_stock = request.POST.get('min_stock', 10)
        expiry = request.POST.get('expiry')
        
        Medicine.objects.create(
            name=name,
            price=price,
            stock_quantity=stock,
            min_stock_level=min_stock,
            expiry_date=expiry
        )
        messages.success(request, f"Added {name} to inventory.")
        return redirect('pharmacy_inventory')
    
    return render(request, 'pharmacy/add_medicine.html')

def edit_medicine(request, medicine_id):
    """View to edit existing medicine."""
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    if request.method == 'POST':
        medicine.name = request.POST.get('name')
        medicine.price = request.POST.get('price')
        medicine.stock_quantity = request.POST.get('stock')
        medicine.min_stock_level = request.POST.get('min_stock')
        medicine.expiry_date = request.POST.get('expiry')
        medicine.save()
        
        messages.success(request, f"Updated {medicine.name}.")
        return redirect('pharmacy_inventory')
        
    return render(request, 'pharmacy/edit_medicine.html', {'medicine': medicine})

def dispense_medicine(request, medicine_id):
    """
    Manually dispense medicine (reduce stock).
    Usage: Staff clicks '-' on inventory page.
    """
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if medicine.stock_quantity > 0:
        medicine.stock_quantity -= 1
        medicine.save()
        messages.success(request, f"Dispensed 1 unit of {medicine.name}")
    else:
        messages.error(request, f"{medicine.name} is out of stock!")
    return redirect('pharmacy_inventory')
def pharmacy_analytics(request):
    """
    Pharmacy Analytics and Predictions view.
    """
    # 1. Sales Trend (Daily for last 30 days)
    today = date.today()
    start_date = today - timedelta(days=30)
    sales_data = PharmacyBill.objects.filter(created_at__date__gte=start_date)\
        .annotate(day=TruncDate('created_at'))\
        .values('day')\
        .annotate(total=Sum('total_amount'))\
        .order_by('day')
    
    sales_labels = [d['day'].strftime('%d %b') if hasattr(d['day'], 'strftime') else str(d['day']) for d in sales_data]
    sales_values = [float(d['total']) for d in sales_data]

    # 2. Inventory Health (Low Stock)
    low_stock = Medicine.objects.filter(stock_quantity__lte=F('min_stock_level'))
    
    # 3. Top Medicines (By Quantity Sold)
    top_selling = BillItem.objects.values('medicine__name')\
        .annotate(total_qty=Sum('quantity'))\
        .order_by('-total_qty')[:5]
    
    # 4. Demand Predictions
    # Using visit-based medicine data for predictions if available
    visits = Visit.objects.exclude(medicines='').values('visit_date', 'medicines')
    predictions = {}
    if visits.exists():
        v_df = pd.DataFrame(list(visits))
        v_df.rename(columns={'visit_date': 'visit_date'}, inplace=True) # Ensure column name match
        predictions = predict_medicine_demand_from_df(v_df)

    context = {
        'sales_chart_labels': json.dumps(sales_labels),
        'sales_chart_values': json.dumps(sales_values),
        'low_stock': low_stock,
        'top_selling': top_selling,
        'predictions': predictions,
    }
    return render(request, 'pharmacy/analytics.html', context)

def print_bill(request, bill_id):
    """
    View for a printable invoice.
    """
    from .models import PharmacyBill
    bill = get_object_or_404(PharmacyBill, id=bill_id)
    return render(request, 'pharmacy/print_bill.html', {'bill': bill})
