
import csv
import random
import datetime
import os
import calendar
from faker import Faker

# Initialize Faker
fake = Faker('en_IN')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCTORS_CSV = os.path.join(BASE_DIR, 'doctors.csv')
PATIENTS_CSV = os.path.join(BASE_DIR, 'patients.csv')
VISITS_CSV = os.path.join(BASE_DIR, 'visits.csv')

def load_doctors():
    doctors = {}
    if os.path.exists(DOCTORS_CSV):
        with open(DOCTORS_CSV, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dept = row['department']
                name = row['doctor_name']
                if dept and name:
                    doctors.setdefault(dept, []).append(name)
    return doctors

def get_existing_patients():
    pids = []
    if os.path.exists(PATIENTS_CSV):
        with open(PATIENTS_CSV, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pids.append(row['patient_id'])
    return pids

def get_weighted_date(year_weights, dept):
    """
    Generate a date based on Year weights AND Department Seasonality.
    """
    # 1. Pick Year
    years = list(year_weights.keys())
    weights = list(year_weights.values())
    year = random.choices(years, weights=weights, k=1)[0]
    
    # 2. Pick Month based on Dept Seasonality
    # Default Profile (Standard)
    # Jan-Dec weights
    month_weights = [1.0] * 12 
    
    # SEASONAL LOGIC
    if dept in ["ENT", "Child Care (Paediatrics)", "General Medicine"]:
        # Winter Flu Peak (Nov, Dec, Jan, Feb)
        month_weights = [
            1.4, 1.3, 1.0, 0.9, 0.8, 0.7, # Jan-Jun
            0.7, 0.8, 0.9, 1.0, 1.3, 1.5  # Jul-Dec (Peak end of year)
        ]
    elif dept in ["Orthopaedics"]:
        # Summer/Outdoor Peak (May-Aug)
        month_weights = [
            0.8, 0.8, 0.9, 1.0, 1.3, 1.4, # Jan-Jun
            1.4, 1.3, 1.0, 0.9, 0.8, 0.8  # Jul-Dec
        ]
    elif dept in ["Emergency"]:
        # Holiday spikes (Dec, Jan) + Summer
        month_weights = [
             1.3, 1.0, 1.0, 1.0, 1.1, 1.2,
             1.2, 1.1, 1.0, 1.0, 1.1, 1.4
        ]
    
    month = random.choices(range(1, 13), weights=month_weights, k=1)[0]
    
    # 3. Pick Day
    _, num_days = calendar.monthrange(year, month)
    day = random.randint(1, num_days)
    
    return datetime.date(year, month, day).isoformat()

def generate_data():
    doctors_map = load_doctors()
    departments = list(doctors_map.keys())
    
    if not departments:
        print("Error: No doctors found.")
        return

    # --- 1. Scale Up Patients (Target 10000) ---
    existing_pids = get_existing_patients()
    target_patients = 10000
    
    if len(existing_pids) < target_patients:
        needed = target_patients - len(existing_pids)
        print(f"Adding {needed} new patients...")
        
        last_id = 0
        if existing_pids:
            try:
                # Handle possible non-integer suffixes gracefully
                pids_numeric = []
                for p in existing_pids:
                    if p.startswith('BMH'):
                        try:
                            pids_numeric.append(int(p.replace('BMH', '')))
                        except ValueError:
                            pass
                if pids_numeric:
                    last_id = max(pids_numeric)
            except Exception:
                pass
            
        new_patients = []
        for i in range(needed):
            pid = f"BMH{last_id + i + 1:04d}"
            new_patients.append([pid, fake.name(), "", random.randint(1, 90)])
            existing_pids.append(pid)
            
        with open(PATIENTS_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if os.stat(PATIENTS_CSV).st_size == 0:
                 writer.writerow(['patient_id', 'patient_name', 'doctor', 'age'])
            writer.writerows(new_patients)

    # --- 2. Generate Ultra-Realistic Visits (80,000) ---
    num_visits = 80000
    print(f"Generating {num_visits} realistic visits...")

    # Expanded Clinical Mappings
    DEPT_DATA = {
        "Cardiology": {
            "symptoms": ["Chest Pain", "Palpitations", "Shortness of breath", "Dizziness", "Fatigue", "Swelling in legs", "Rapid Heartbeat", "Fainting", "High Blood Pressure"],
            "medicines": ["Amlodipine", "Atorvastatin", "Aspirin", "Metoprolol", "Lisinopril", "Losartan", "Clopidogrel", "Furosemide", "Rosuvastatin", "Digoxin", "Warfarin", "Hydrochlorothiazide", "Carvedilol", "Nitroglycerin", "Spironolactone"]
        },
        "Gastroenterology": {
            "symptoms": ["Abdominal Pain", "Nausea", "Vomiting", "Heartburn", "Bloating", "Constipation", "Diarrhea", "Indigestion", "Loss of Appetite", "Blood in Stool"],
            "medicines": ["Omeprazole", "Pantoprazole", "Metformin", "Ranitidine", "Domperidone", "Lactulose", "Esomeprazole", "Loperamide", "Ondansetron", "Psyllium", "Dicyclomine", "Probiotics", "Sucralfate"]
        },
        "Neurosciences": {
            "symptoms": ["Headache", "Seizures", "Migraine", "Dizziness", "Numbness", "Memory Loss", "Tremors", "Confusion", "Vision Problems", "Slurred Speech"],
            "medicines": ["Gabapentin", "Topiramate", "Levetiracetam", "Sertraline", "Donepezil", "Amitriptyline", "Pregabalin", "Carbamazepine", "Lamotrigine", "Sumatriptan", "Valproic Acid", "Baclofen", "Memantine"]
        },
        "Orthopaedics": {
            "symptoms": ["Joint Pain", "Back Pain", "Fracture", "Muscle Pain", "Stiffness", "Swelling", "Shoulder Pain", "Knee Pain", "Hip Pain", "Sprain"],
            "medicines": ["Ibuprofen", "Paracetamol", "Calcium", "Vitamin D3", "Tramadol", "Diclofenac", "Methocarbamol", "Naproxen", "Celecoxib", "Glucosamine", "Codeine", "Meloxicam", "Cyclobenzaprine"]
        },
        "Child Care (Paediatrics)": {
            "symptoms": ["Fever", "Cough", "Cold", "Rash", "Vomiting", "Ear Pain", "Crying", "Stomach Ache", "Wheezing", "Runny Nose"],
            "medicines": ["Paracetamol Syrup", "Amoxicillin", "Ibuprofen Syrup", "Cetirizine", "Oral Rehydration Salts", "Azithromycin", "Cefixime", "Montelukast", "Saline Drops", "Zinc Syrup", "Multivitamins"]
        },
        "ENT": {
            "symptoms": ["Sore Throat", "Ear Pain", "Nasal Congestion", "Hearing Loss", "Tinnitus", "Vertigo", "Hoarseness", "Snoring"],
            "medicines": ["Cetirizine", "Nasal Spray", "Amoxicillin", "Paracetamol", "Loratadine", "Pseudoephedrine", "Fluticasone", "Oxymetazoline", "Ciprofloxacin Drops", "Clarithromycin"]
        },
        "Oncology": {
            "symptoms": ["Fatigue", "Weight Loss", "Lump", "Pain", "Night Sweats", "Anemia", "Loss of Appetite"],
            "medicines": ["Tramadol", "Morphine", "Ondansetron", "Prednisone", "Tamoxifen", "Letrozole", "Dexamethasone", "Methotrexate", "Fentanyl", "Filgrastim"]
        },
        "Women's Care (Obstetrics & Gynaecology)": {
            "symptoms": ["Cramps", "Irregular Periods", "Pregnancy Checkup", "Pelvic Pain", "Mood Swings", "Hot Flashes"],
            "medicines": ["Folic Acid", "Iron Supplements", "Progesterone", "Ibuprofen", "Clomiphene", "Estradiol", "Metronidazole", "Fluconazole", "Calcium Carbonate", "Prenatal Vitamins"]
        },
        "Radiology": {
             "symptoms": ["Injury", "Chest Pain", "Fracture", "Abdominal Pain", "Head Injury"],
             "medicines": ["Contrast Dye", "Pain Relief", "Sedative"]
        },
        "Emergency": {
            "symptoms": ["Chest Pain", "Accident", "Breathing Difficulty", "Severe Pain", "Burn", "Poisoning", "Trauma"],
            "medicines": ["Morphine", "Epinephrine", "Saline", "Paracetamol IV", "Ketorolac", "Insulin", "Atropine", "Diazepam", "Hydrocortisone"]
        },
        "Critical Care": {
            "symptoms": ["Unconscious", "Low BP", "Respiratory Failure", "Sepsis", "Organ Failure"],
            "medicines": ["Norepinephrine", "Sedatives", "Antibiotics IV", "Dopamine", "Heparin", "Furosemide IV", "Midazolam"]
        }
    }
    
    DEFAULT_DATA = {
        "symptoms": ["Fever", "Pain", "Weakness"],
        "medicines": ["Paracetamol", "Vitamins"]
    }

    case_types = ["Normal", "Emergency", "Critical"]
    
    # Year weights: Strong growth
    year_weights = {2024: 0.35, 2025: 0.65}

    # Define high-load departments (Cardiology, Orthopaedics)
    all_docs_flat = []
    for dept, docs in doctors_map.items():
        for d in docs:
            all_docs_flat.append((d, dept))
            
    # Load Balancing (Skewed)
    weighted_docs = []
    for d, dept in all_docs_flat:
        if dept in ["Cardiology", "Orthopaedics", "Child Care (Paediatrics)"]:
            weighted_docs.extend([(d, dept)] * 4) # 4x load
        else:
            weighted_docs.append((d, dept))

    new_visits = []
    for _ in range(num_visits):
        pid = random.choice(existing_pids)
        # Pick Weighted Doctor
        doc_name, dept = random.choice(weighted_docs)
        
        # Clinical Data based on Dept
        dept_info = DEPT_DATA.get(dept, DEFAULT_DATA)
        
        ctype = random.choices(case_types, weights=[0.80, 0.15, 0.05])[0]
        vdate = get_weighted_date(year_weights, dept)
        
        sym_count = random.randint(1, 3)
        syms = ", ".join(random.sample(dept_info["symptoms"], k=min(sym_count, len(dept_info["symptoms"]))))
        
        med_count = random.randint(1, 3)
        meds = ", ".join(random.sample(dept_info["medicines"], k=min(med_count, len(dept_info["medicines"]))))
        
        new_visits.append([pid, dept, doc_name, ctype, vdate, meds, syms])

    # Sort visits by date for realism
    new_visits.sort(key=lambda x: x[4])

    with open(VISITS_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['patient_id', 'department', 'doctor', 'case_type', 'visit_date', 'medicines', 'symptoms'])
        writer.writerows(new_visits)

    print("Successfully generated realistic dataset.")

if __name__ == "__main__":
    generate_data()
