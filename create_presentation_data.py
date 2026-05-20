import os
import django
import random
from datetime import timedelta, date, datetime
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Visit, Doctor, Patient, Department
from pharmacy.models import Medicine, PrescriptionLine, PharmacyBill, BillItem

def generate_perfect_data():
    today = date.today()
    now_dt = datetime.now()

    print("Fetching active records...")
    doctors = list(Doctor.objects.all()[:20])  # Use 20 doctors
    patients = list(Patient.objects.all()[:500])
    medicines = list(Medicine.objects.all()[:50])
    
    if not doctors or not patients or not medicines:
        print("Error: Missing basic records (Doctors/Patients/Medicines). Run standard seeds first.")
        return

    case_types = ["Normal", "Follow-up", "Emergency", "Critical"]
    case_weights = [50, 30, 15, 5]

    visits_created = 0
    bills_created = 0

    print("Generating beautifully distributed presentation data for the last 30 days...")

    # We will generate between 1500 and 2000 total visits spread across the last 30 days
    # Increasing trend towards today makes graphs look amazing (upward trajectory)
    
    for day_offset in range(30, -1, -1): # 30 days ago up to today (0)
        current_date = today - timedelta(days=day_offset)
        
        # Base visits 30, plus increasing trend, plus some random noise
        # E.g. day 30 ago -> ~30 visits. Today -> ~100 visits.
        visits_today = int(30 + (30 - day_offset) * 2.5 + random.randint(-10, 10))
        visits_today = max(10, visits_today) # Ensure at least 10 visits

        for _ in range(visits_today):
            doc = random.choice(doctors)
            pat = random.choice(patients)
            case_t = random.choices(case_types, weights=case_weights)[0]
            
            # Select 1-3 random medicines
            num_meds = random.randint(1, 4)
            prescribed_meds = random.sample(medicines, num_meds)
            
            med_names = [m.name for m in prescribed_meds]
            meds_string = ", ".join(f"{name} x{random.randint(1,2)}" for name in med_names)

            # Create the Visit
            visit = Visit.objects.create(
                patient=pat,
                department=doc.department,
                doctor=doc,
                case_type=case_t,
                visit_date=current_date,
                medicines=meds_string,
                symptoms="Generated for Presentation",
                slot="10:00 - 10:15"
            )
            visits_created += 1

            # Save Prescription Lines
            for m in prescribed_meds:
                qty = random.randint(1, 3)
                PrescriptionLine.objects.create(
                    visit=visit,
                    medicine=m,
                    quantity=qty,
                    dosage_instructions="1-0-1"
                )

            # Create Pharmacy Bill ~80% of the time
            if random.random() < 0.8:
                subtotal = sum(m.price * qty for m in prescribed_meds)
                tax = subtotal * Decimal('0.05') # 5% tax
                total = subtotal + tax

                bill = PharmacyBill.objects.create(
                    customer_name=pat.patient_name,
                    patient=pat,
                    subtotal=subtotal,
                    tax_percentage=Decimal('5.00'),
                    tax_amount=tax,
                    discount_percentage=Decimal('0.00'),
                    discount_amount=Decimal('0.00'),
                    total_amount=total
                )
                
                # Update timestamp manually since auto_now_add locked it
                target_datetime = now_dt - timedelta(days=day_offset, hours=random.randint(0,8))
                PharmacyBill.objects.filter(id=bill.id).update(created_at=target_datetime)
                
                # Add Bill items
                for m in prescribed_meds:
                    BillItem.objects.create(
                        bill=bill,
                        medicine=m,
                        quantity=qty,
                        price_per_unit=m.price,
                        total_price=m.price * qty
                    )
                bills_created += 1

    print(f"\n✨ Generated {visits_created} visits perfectly scaled over 30 days!")
    print(f"✨ Generated {bills_created} associated pharmacy bills!")
    print("\nPresentation data is locked, loaded, and visually stunning!")

if __name__ == '__main__':
    generate_perfect_data()
