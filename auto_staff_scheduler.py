import csv
import random

DOCTOR_SHIFTS = [
    ("Morning", "06:00", "12:00"),
    ("Afternoon", "12:00", "18:00"),
    ("Evening", "18:00", "23:59"),
    ("Night", "00:00", "06:00")
]

NURSE_SHIFTS = [
    ("Morning", "07:00", "15:00"),
    ("Overview", "15:00", "23:00"), 
    ("Night", "23:00", "07:00")
]
# Note: "Overview" typo in my logic? Standard is Morning/Evening/Night. 
# Checking logic: Morning, Evening, Night. Correcting list below.
NURSE_SHIFTS = [
    ("Morning", "07:00", "15:00"),
    ("Evening", "15:00", "23:00"), 
    ("Night", "23:00", "07:00")
]

DEPARTMENTS_FILE = 'departments.csv'
DOCTORS_FILE = 'doctors.csv'
NURSES_FILE = 'nurses.csv'

def load_csv(filename):
    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

def save_csv(filename, fieldnames, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_doctor(dept, idx, staff_id):
    return {
        "staff_id": staff_id,
        "department": dept,
        "doctor_name": f"Dr. New Hire {idx}",
        "gender": "Female" if random.choice([True, False]) else "Male",
        "qualifications": "MBBS",
        "email": f"drnew{idx}@bmh.com",
        "phone": f"+91 {random.randint(6000000000, 9999999999)}",
        "specialization": "General",
        "shift_start": "09:00",
        "shift_end": "17:00",
        "work_days": "Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        "shift_type": "Morning",
        "slot_duration": "15",
        "max_patients": "25"
    }

def generate_nurse(dept, idx, staff_id):
    return {
        "staff_id": staff_id,
        "department": dept,
        "nurse_name": f"Nurse New Hire {idx}",
        "gender": "Female" if random.choice([True, False]) else "Male",
        "qualifications": "B.Sc Nursing",
        "email": f"nursenew{idx}@bmh.com",
        "phone": f"+91 {random.randint(6000000000, 9999999999)}",
        "shift_start": "07:00",
        "shift_end": "15:00",
        "work_days": "Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        "shift_type": "Morning"
    }

WORK_PATTERNS = [
    "Mon,Tue,Wed,Thu,Fri",
    "Tue,Wed,Thu,Fri,Sat",
    "Wed,Thu,Fri,Sat,Sun",
    "Thu,Fri,Sat,Sun,Mon",
    "Fri,Sat,Sun,Mon,Tue",
    "Sat,Sun,Mon,Tue,Wed",
    "Sun,Mon,Tue,Wed,Thu"
]

def process_scheduling():
    depts = [row['name'] for row in load_csv(DEPARTMENTS_FILE)]
    docs = load_csv(DOCTORS_FILE)
    nurses = load_csv(NURSES_FILE)
    
    print("--- Scheduling Doctors ---")
    new_docs = []
    doc_id_counter = 1000
    
    # Find max existing doctor ID
    max_doc_id = 0
    for d in docs:
        if d.get('staff_id', '').startswith('DOC'):
            try:
                num = int(d['staff_id'][3:])
                max_doc_id = max(max_doc_id, num)
            except:
                pass
    
    for dept in depts:
        dept_docs = [d for d in docs if d['department'] == dept]
        
        # Ensure min coverage for 24/7 with 5-day weeks
        # To guarantee overlap across 4 shifts * 5-day patterns, we need safe margin.
        # Mathematical trace shows 8 doctors ensures coverage for Night shift gaps.
        while len(dept_docs) < 8:
            print(f"Adding doctor to {dept}")
            max_doc_id += 1
            staff_id = f"DOC{max_doc_id:03d}"
            new_doc = generate_doctor(dept, doc_id_counter, staff_id)
            dept_docs.append(new_doc)
            docs.append(new_doc)
            doc_id_counter += 1
            
        # Distribute shifts and day patterns
        for i, doc in enumerate(dept_docs):
            shift_name, start, end = DOCTOR_SHIFTS[i % 4]
            pattern = WORK_PATTERNS[i % 7]
            
            doc['shift_type'] = shift_name
            doc['shift_start'] = start
            doc['shift_end'] = end
            doc['work_days'] = pattern
            
    print("--- Scheduling Nurses ---")
    nurse_id_counter = 1000
    
    # Find max existing nurse ID
    max_nurse_id = 0
    for n in nurses:
        if n.get('staff_id', '').startswith('NUR'):
            try:
                num = int(n['staff_id'][3:])
                max_nurse_id = max(max_nurse_id, num)
            except:
                pass
    
    for dept in depts:
        dept_nurses = [n for n in nurses if n['department'] == dept]
        
        # Ensure min coverage for 24/7 with 5-day weeks
        # 3 shifts. Trace shows 6 nurses ensures coverage.
        while len(dept_nurses) < 6:
            print(f"Adding nurse to {dept}")
            max_nurse_id += 1
            staff_id = f"NUR{max_nurse_id:03d}"
            new_nurse = generate_nurse(dept, nurse_id_counter, staff_id)
            dept_nurses.append(new_nurse)
            nurses.append(new_nurse)
            nurse_id_counter += 1
            
        # Distribute shifts and day patterns
        for i, nurse in enumerate(dept_nurses):
            shift_name, start, end = NURSE_SHIFTS[i % 3]
            pattern = WORK_PATTERNS[i % 7]
            
            nurse['shift_type'] = shift_name
            nurse['shift_start'] = start
            nurse['shift_end'] = end
            nurse['work_days'] = pattern

    # Save
    if docs:
        save_csv(DOCTORS_FILE, docs[0].keys(), docs)
    if nurses:
        save_csv(NURSES_FILE, nurses[0].keys(), nurses)
        
    print("✅ Scheduling Complete!")

if __name__ == "__main__":
    process_scheduling()
