import os
import django
import random
from datetime import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Department, Doctor, Nurse

# SMSR Constants
DOCTOR_SHIFTS = [
    ("Morning", time(6, 0), time(12, 0)),
    ("Afternoon", time(12, 0), time(18, 0)),
    ("Evening", time(18, 0), time(23, 59)),
    ("Night", time(0, 0), time(6, 0))
]

NURSE_SHIFTS = [
    ("Morning", time(7, 0), time(15, 0)),
    ("Evening", time(15, 0), time(23, 0)), 
    ("Night", time(23, 0), time(7, 0))
]

WORK_PATTERNS = [
    "Mon,Tue,Wed,Thu,Fri",
    "Tue,Wed,Thu,Fri,Sat",
    "Wed,Thu,Fri,Sat,Sun",
    "Thu,Fri,Sat,Sun,Mon",
    "Fri,Sat,Sun,Mon,Tue",
    "Sat,Sun,Mon,Tue,Wed",
    "Sun,Mon,Tue,Wed,Thu"
]

def get_max_id(model, prefix):
    max_id = 0
    for obj in model.objects.all():
        if obj.staff_id.startswith(prefix):
            try:
                num = int(obj.staff_id[len(prefix):])
                max_id = max(max_id, num)
            except:
                pass
    return max_id

def ensure_min_staff():
    """Ensure each department has min staff for 24/7 SMSR coverage"""
    depts = Department.objects.all()
    max_doc_id = get_max_id(Doctor, "DOC")
    max_nurse_id = get_max_id(Nurse, "NUR")

    for dept in depts:
        # Doctors (Need 8 for redundant 24/7 coverage)
        dept_docs = Doctor.objects.filter(department=dept)
        while dept_docs.count() < 8:
            max_doc_id += 1
            staff_id = f"DOC{max_doc_id:03d}"
            Doctor.objects.create(
                staff_id=staff_id,
                department=dept,
                doctor_name=f"Dr. SMSR-{max_doc_id}",
                gender=random.choice(["Male", "Female"]),
                qualifications="MBBS, MD",
                email=f"smsr_doc{max_doc_id}@bmh.com",
                phone=f"+91 {random.randint(6000000000, 9999999999)}",
                specialization="General Medicine",
                shift_start=time(9, 0),
                shift_end=time(17, 0),
                work_days="Mon,Tue,Wed,Thu,Fri",
                shift_type="Morning",
                slot_duration=15,
                max_patients=25
            )
            print(f"Added Doctor {staff_id} to {dept.name}")

        # Nurses (Need 6 for redundant 24/7 coverage)
        dept_nurses = Nurse.objects.filter(department=dept)
        while dept_nurses.count() < 6:
            max_nurse_id += 1
            staff_id = f"NUR{max_nurse_id:03d}"
            Nurse.objects.create(
                staff_id=staff_id,
                department=dept,
                nurse_name=f"Nurse SMSR-{max_nurse_id}",
                gender=random.choice(["Male", "Female"]),
                qualifications="B.Sc Nursing",
                email=f"smsr_nurse{max_nurse_id}@bmh.com",
                phone=f"+91 {random.randint(6000000000, 9999999999)}",
                shift_start=time(7, 0),
                shift_end=time(15, 0),
                work_days="Mon,Tue,Wed,Thu,Fri",
                shift_type="Morning"
            )
            print(f"Added Nurse {staff_id} to {dept.name}")

def apply_smsr():
    """Apply SMSR modulo-based scheduling logic"""
    depts = Department.objects.all()
    
    for dept in depts:
        print(f"Applying SMSR to {dept.name}...")
        
        # Distribute Doctors
        docs = Doctor.objects.filter(department=dept).order_by('staff_id')
        for i, doc in enumerate(docs):
            shift_idx = i % 4
            pattern_idx = i % 7
            
            s_name, s_start, s_end = DOCTOR_SHIFTS[shift_idx]
            doc.shift_type = s_name
            doc.shift_start = s_start
            doc.shift_end = s_end
            doc.work_days = WORK_PATTERNS[pattern_idx]
            doc.save()
            
        # Distribute Nurses
        nurses = Nurse.objects.filter(department=dept).order_by('staff_id')
        for i, nurse in enumerate(nurses):
            shift_idx = i % 3
            pattern_idx = i % 7
            
            s_name, s_start, s_end = NURSE_SHIFTS[shift_idx]
            nurse.shift_type = s_name
            nurse.shift_start = s_start
            nurse.shift_end = s_end
            nurse.work_days = WORK_PATTERNS[pattern_idx]
            nurse.save()

if __name__ == "__main__":
    ensure_min_staff()
    apply_smsr()
    print("🚀 SMSR Algorithm implementation complete!")
