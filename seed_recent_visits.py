import os
import django
import random
from datetime import timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Visit, Doctor, Patient, Department

today = date.today()
print("Seeding recent visits for all doctors...")

# Get all doctors
doctors = Doctor.objects.all()

patients = list(Patient.objects.all()[:1000])

new_visits = []

case_types = ["Normal", "Emergency", "Critical"]

for doc in doctors:
    # Give every doctor 5-15 visits in the last 7 days
    for i in range(15):
        visit_date = today - timedelta(days=random.randint(0, 6))
        pat = random.choice(patients)
        case_t = random.choices(case_types, weights=[70, 20, 10])[0]
        
        new_visits.append(Visit(
            patient=pat,
            department=doc.department,
            doctor=doc,
            case_type=case_t,
            visit_date=visit_date,
            medicines="Paracetamol, Amoxicillin",
            symptoms="Fever, Cough",
            slot="10:00 - 10:15"
        ))

Visit.objects.bulk_create(new_visits)
print(f"Created {len(new_visits)} visits in the last 7 days.")
