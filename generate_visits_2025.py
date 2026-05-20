import csv, random, datetime, os

BASE = os.path.abspath(os.path.dirname(__file__))
DOCTORS_CSV = os.path.join(BASE, 'doctors.csv')
VISITS_CSV = os.path.join(BASE, 'visits.csv')

# Load doctors per department
dept_doctors = {}
with open(DOCTORS_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dept = row['department']
        doc = row['doctor_name']
        dept_doctors.setdefault(dept, []).append(doc)

departments = list(dept_doctors.keys())
case_types = ['Normal', 'Emergency', 'Critical']
medicines_list = ['Aspirin', 'Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Metformin']

num_visits = 2000  # generate 2000 visit records

with open(VISITS_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['patient_id', 'department', 'doctor', 'case_type', 'visit_date', 'medicines'])
    for _ in range(num_visits):
        patient_id = f"BMH{random.randint(1, 1000):04d}"
        dept = random.choice(departments)
        doctor = random.choice(dept_doctors[dept])
        case_type = random.choice(case_types)
        # random date in 2025
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # simplify to avoid month length issues
        visit_date = datetime.date(2025, month, day).isoformat()
        medicines = random.choice(medicines_list)
        writer.writerow([patient_id, dept, doctor, case_type, visit_date, medicines])
print('Generated', num_visits, 'visits in', VISITS_CSV)
