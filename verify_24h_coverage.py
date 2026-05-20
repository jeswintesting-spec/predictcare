import os
import django
from collections import defaultdict

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Department, Doctor, Nurse

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DOCTOR_SHIFTS = ["Morning", "Afternoon", "Evening", "Night"]
NURSE_SHIFTS = ["Morning", "Evening", "Night"]

def verify_coverage():
    departments = Department.objects.all()
    all_pass = True

    print(f"{'Department':<40} | {'Docs 24/7':<10} | {'Nurses 24/7':<10}")
    print("-" * 66)

    for dept in departments:
        # Check Doctors
        doc_coverage = defaultdict(set) # (day, shift) -> docs
        doctors = Doctor.objects.filter(department=dept)
        for doc in doctors:
            work_days = doc.work_days.split(',')
            for day in work_days:
                doc_coverage[(day, doc.shift_type)].add(doc.staff_id)
        
        docs_ok = True
        for day in DAYS:
            for shift in DOCTOR_SHIFTS:
                if not doc_coverage[(day, shift)]:
                    docs_ok = False
                    break
        
        # Check Nurses
        nurse_coverage = defaultdict(set)
        nurses = Nurse.objects.filter(department=dept)
        for nurse in nurses:
            work_days = nurse.work_days.split(',')
            for day in work_days:
                nurse_coverage[(day, nurse.shift_type)].add(nurse.staff_id)
        
        nurses_ok = True
        for day in DAYS:
            for shift in NURSE_SHIFTS:
                if not nurse_coverage[(day, shift)]:
                    nurses_ok = False
                    break
        
        print(f"{dept.name:<40} | {'✅' if docs_ok else '❌':<10} | {'✅' if nurses_ok else '❌':<10}")
        if not docs_ok or not nurses_ok:
            all_pass = False

    if all_pass:
        print("\n✨ ALL DEPARTMENTS HAVE 24/7 COVERAGE!")
    else:
        print("\n⚠️ SOME DEPARTMENTS LACK FULL COVERAGE.")

if __name__ == "__main__":
    verify_coverage()
