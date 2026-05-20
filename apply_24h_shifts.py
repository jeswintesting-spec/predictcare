import os
import django
import csv
from datetime import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Department, Doctor, Nurse

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

def apply_shifts():
    departments = Department.objects.all()
    
    print(f"Processing {departments.count()} departments...")

    for dept in departments:
        # 1. Update Doctors (4-shift system)
        doctors = Doctor.objects.filter(department=dept).order_by('staff_id')
        for i, doc in enumerate(doctors):
            shift_name, start, end = DOCTOR_SHIFTS[i % 4]
            pattern = WORK_PATTERNS[i % 7]
            
            doc.shift_type = shift_name
            doc.shift_start = start
            doc.shift_end = end
            doc.work_days = pattern
            doc.save()
            
        # 2. Update Nurses (3-shift system)
        nurses = Nurse.objects.filter(department=dept).order_by('staff_id')
        for i, nurse in enumerate(nurses):
            shift_name, start, end = NURSE_SHIFTS[i % 3]
            pattern = WORK_PATTERNS[i % 7]
            
            nurse.shift_type = shift_name
            nurse.shift_start = start
            nurse.shift_end = end
            nurse.work_days = pattern
            nurse.save()
            
    print("✅ Database updated successfully.")

def sync_csv():
    # Sync Doctors
    doctors = Doctor.objects.all().order_by('staff_id')
    if doctors.exists():
        fieldnames = [
            'staff_id', 'department', 'doctor_name', 'gender', 'qualifications', 
            'email', 'phone', 'specialization', 'shift_start', 'shift_end', 
            'work_days', 'shift_type', 'slot_duration', 'max_patients'
        ]
        with open('doctors.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for doc in doctors:
                writer.writerow({
                    'staff_id': doc.staff_id,
                    'department': doc.department.name,
                    'doctor_name': doc.doctor_name,
                    'gender': doc.gender,
                    'qualifications': doc.qualifications,
                    'email': doc.email,
                    'phone': doc.phone,
                    'specialization': doc.specialization,
                    'shift_start': doc.shift_start.strftime('%H:%M'),
                    'shift_end': doc.shift_end.strftime('%H:%M'),
                    'work_days': doc.work_days,
                    'shift_type': doc.shift_type,
                    'slot_duration': doc.slot_duration,
                    'max_patients': doc.max_patients
                })
        print("✅ doctors.csv synchronized.")

    # Sync Nurses
    nurses = Nurse.objects.all().order_by('staff_id')
    if nurses.exists():
        fieldnames = [
            'staff_id', 'department', 'nurse_name', 'gender', 'qualifications', 
            'email', 'phone', 'shift_start', 'shift_end', 'work_days', 'shift_type'
        ]
        with open('nurses.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for nurse in nurses:
                writer.writerow({
                    'staff_id': nurse.staff_id,
                    'department': nurse.department.name,
                    'nurse_name': nurse.nurse_name,
                    'gender': nurse.gender,
                    'qualifications': nurse.qualifications,
                    'email': nurse.email,
                    'phone': nurse.phone,
                    'shift_start': nurse.shift_start.strftime('%H:%M'),
                    'shift_end': nurse.shift_end.strftime('%H:%M'),
                    'work_days': nurse.work_days,
                    'shift_type': nurse.shift_type
                })
        print("✅ nurses.csv synchronized.")

if __name__ == "__main__":
    apply_shifts()
    sync_csv()
    print("🚀 24/7 Shift Rotation implementation complete!")
