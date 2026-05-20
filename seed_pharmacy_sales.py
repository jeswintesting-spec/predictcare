
import os
import random
import datetime
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from pharmacy.models import Medicine, PharmacyBill, BillItem
from hospital.models import Patient

def seed_sales():
    print("Seeding Pharmacy Sales Data (Last 30 days)...")
    
    medicines = list(Medicine.objects.all())
    if not medicines:
        print("Error: No medicines found. Run seed_pharmacy_inventory.py first.")
        return

    patients = list(Patient.objects.all())
    
    today = datetime.date.today()
    
    # Clear existing sales data to avoid duplicates
    print("Clearing existing sales data...")
    BillItem.objects.all().delete()
    PharmacyBill.objects.all().delete()

    for i in range(30):
        target_date = today - datetime.timedelta(days=i)
        
        # Number of bills per day (random 5-15)
        num_bills = random.randint(5, 15)
        
        for _ in range(num_bills):
            # Select random patient or walk-in
            patient = random.choice(patients) if patients and random.random() > 0.3 else None
            customer_name = patient.patient_name if patient else f"Walk-in Customer {random.randint(100, 999)}"
            
            # Create Bill
            bill = PharmacyBill.objects.create(
                customer_name=customer_name,
                patient=patient,
                total_amount=0
            )
            
            # Add 1-5 random items to bill
            num_items = random.randint(1, 5)
            bill_total = Decimal('0.00')
            
            selected_meds = random.sample(medicines, min(len(medicines), num_items))
            for med in selected_meds:
                qty = random.randint(1, 3)
                price = med.price
                item_total = price * qty
                
                BillItem.objects.create(
                    bill=bill,
                    medicine=med,
                    quantity=qty,
                    price_per_unit=price,
                    total_price=item_total
                )
                bill_total += item_total
                
            # Update bill total
            bill.total_amount = bill_total
            bill.save()

            # FINALLY set the created_at to the target_date
            # Doing this AFTER save() ensures it's not overwritten by the in-memory object
            PharmacyBill.objects.filter(id=bill.id).update(created_at=datetime.datetime.combine(target_date, datetime.time(random.randint(9, 18), random.randint(0, 59))))

            
    print("Done. Pharmacy sales data seeded.")

if __name__ == "__main__":
    seed_sales()
