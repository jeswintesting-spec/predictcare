
import csv
import random
import datetime
import os
import calendar
from faker import Faker

# Initialize Faker
fake = Faker('en_IN')

# Configuration
# "Yesterday" or today. We'll use today for up-to-date data.
TARGET_END_DATE = datetime.date.today()
START_DATE_2024 = datetime.date(2024, 1, 1)

NUM_VISITS = 100000 
TARGET_PATIENTS = 5000

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
                staff_id = row['staff_id']
                name = row['doctor_name']
                if dept and staff_id:
                    doctors.setdefault(dept, []).append((staff_id, name))
    return doctors

def get_existing_patients():
    pids = []
    if os.path.exists(PATIENTS_CSV):
        with open(PATIENTS_CSV, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pids.append(row['patient_id'])
    return pids

def get_random_date_between(start_date, end_date, dept):
    """
    Generate a random date, applying seasonality bias.
    """
    delta_days = (end_date - start_date).days
    if delta_days <= 0:
        return start_date

    # Naive random day
    random_days = random.randint(0, delta_days)
    candidate_date = start_date + datetime.timedelta(days=random_days)
    
    # Seasonality Check (Simple Rejection Sampling to bias distribution)
    month = candidate_date.month
    
    weight = 1.0
    
    # 1. Departments with Winter Peaks
    if dept in ["ENT", "Child Care (Paediatrics)", "General Medicine"]:
        if month in [11, 12, 1, 2]: weight = 1.5
        elif month in [6, 7]: weight = 0.6
        
    # 2. Departments with Summer Peaks
    elif dept in ["Orthopaedics", "Dermatology"]: # Injuries, skin issues
        if month in [5, 6, 7, 8]: weight = 1.4
        
    # 3. Overall Growth Trend (Later years = higher weight)
    # 2026 should be busiest, then 2025, then 2024
    if candidate_date.year == 2026: weight *= 1.8
    elif candidate_date.year == 2025: weight *= 1.3
    else: weight *= 0.8 # 2024
    
    # Accept/Reject based on weight
    # Max weight approx 1.5 * 1.8 = 2.7. Normalized accept probability.
    if random.random() * 3.0 < weight:
        return candidate_date
    else:
        # Retry once recursively (simple way to bias without infinite loop)
        # If rejected, just return a purely random one to fill gaps
        return start_date + datetime.timedelta(days=random.randint(0, delta_days))

def generate_data():
    print(f"--- Generating Real Data till {TARGET_END_DATE} ---")
    
    doctors_map = load_doctors()
    departments = list(doctors_map.keys())
    
    if not departments:
        print("Error: No doctors found. Make sure doctors.csv exists.")
        return

    # --- 1. Scale Up Patients ---
    existing_pids = get_existing_patients()
    
    if len(existing_pids) < TARGET_PATIENTS:
        needed = TARGET_PATIENTS - len(existing_pids)
        print(f"Adding {needed} new patients...")
        
        last_id = 0
        if existing_pids:
            try:
                # Find max ID
                numeric_ids = [int(p.replace('BMH', '')) for p in existing_pids if p.startswith('BMH') and p[3:].isdigit()]
                if numeric_ids:
                    last_id = max(numeric_ids)
            except:
                pass
            
        # Malayali Name Components
        malayali_first_names_male = [
            "Rahul", "Arjun", "Vishal", "Sanjay", "Kiran", "Nithin", "Abhilash", "Jitin", "Pranav", "Midhun",
            "Faisal", "Mohammed", "Aneesh", "Thomas", "Jacob", "Mathew", "George", "Varghese", "Antony", "Sebasitan"
        ]
        malayali_first_names_female = [
            "Anjali", "Sreelekshmi", "Meera", "Reshma", "Anupama", "Sneha", "Kavya", "Aiswarya", "Dhanya", "Remya",
            "Fathima", "Sumayya", "Mary", "Ann", "Sherly", "Leelamma", "Mariamma", "Sophy", "Tessa", "Riya"
        ]
        malayali_surnames = [
            "Nair", "Menon", "Pillai", "Kurup", "Panicker", "Nambiar", "Warrier", "Thampi",
            "Varghese", "Kurian", "Chacko", "Joseph", "Abraham", "Philip", "George",
            "Faisal", "Hashim", "Ibrahim", "Siddique", "Rahman"
        ]

        new_patients = []
        for i in range(needed):
            pid = f"BMH{last_id + i + 1:04d}"
            
            # Generate fuller profile
            gender = random.choice(['Male', 'Female'])
            if gender == 'Male':
                fname = random.choice(malayali_first_names_male)
            else:
                fname = random.choice(malayali_first_names_female)
            
            lname = random.choice(malayali_surnames)
            full_name = f"{fname} {lname}"
            
            age = random.randint(1, 90)
            
            # Approximate DOB
            dob_year = 2026 - age
            dob = datetime.date(dob_year, random.randint(1, 12), random.randint(1, 28)).isoformat()
            
            kerala_towns = [
                "Vazhuthacaud, Thiruvananthapuram", "Edapally, Kochi", "Kakkanad, Kochi", "Nadakkavu, Kozhikode",
                "Round North, Thrissur", "Thana, Kannur", "Chinnakada, Kollam", "Mullakkal, Alappuzha",
                "Civil Station, Palakkad", "Down Hill, Malappuram", "Kanjikuzhy, Kottayam", "Vidyanagar, Kasaragod",
                "Munnar, Idukki", "Kalpetta, Wayanad", "Kumbanad, Pathanamthitta", "Pala, Kottayam",
                "Ottapalam, Palakkad", "Nilambur, Malappuram", "Thalassery, Kannur", "Guruvayur, Thrissur"
            ]
            location = random.choice(kerala_towns)
            
            # Schema: patient_id, patient_name, doctor, age, dob, gender, location, assigned_slot
            new_patients.append([pid, full_name, "", age, dob, gender, location, ""])
            existing_pids.append(pid)
            
        # Append mode
        with open(PATIENTS_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if os.stat(PATIENTS_CSV).st_size == 0:
                 writer.writerow(['patient_id', 'patient_name', 'doctor', 'age', 'dob', 'gender', 'location', 'assigned_slot'])
            writer.writerows(new_patients)
    else:
        print(f"Patients count ({len(existing_pids)}) is sufficient.")

    # --- 2. Generate Visits (Replacing old visits.csv completely to ensure clean history) ---
    print(f"Generating {NUM_VISITS} realistic visits from {START_DATE_2024} to {TARGET_END_DATE}...")

    # Expanded Clinical Mappings for all 23 Departments
    DEPT_DATA = {
        "Cardiology": { "symptoms": ["Chest Pain", "Palpitations", "Shortness of breath", "Dizziness", "Fatigue"], "medicines": ["Amlodipine", "Atorvastatin", "Aspirin", "Metoprolol"] },
        "Gastroenterology": { "symptoms": ["Abdominal Pain", "Nausea", "Vomiting", "Heartburn"], "medicines": ["Omeprazole", "Pantoprazole", "Metformin", "Ranitidine"] },
        "Neurosciences": { "symptoms": ["Headache", "Seizures", "Migraine", "Dizziness"], "medicines": ["Gabapentin", "Topiramate", "Levetiracetam"] },
        "Orthopaedics": { "symptoms": ["Joint Pain", "Back Pain", "Fracture", "Muscle Pain"], "medicines": ["Ibuprofen", "Paracetamol", "Calcium", "Vitamin D3"] },
        "Child Care (Paediatrics)": { "symptoms": ["Fever", "Cough", "Cold", "Rash"], "medicines": ["Paracetamol Syrup", "Amoxicillin", "Ibuprofen Syrup"] },
        "ENT": { "symptoms": ["Sore Throat", "Ear Pain", "Nasal Congestion"], "medicines": ["Cetirizine", "Nasal Spray", "Amoxicillin"] },
        "Oncology": { "symptoms": ["Fatigue", "Weight Loss", "Lump", "Pain"], "medicines": ["Tramadol", "Morphine", "Ondansetron"] },
        "Women's Care (Obstetrics & Gynaecology)": { "symptoms": ["Cramps", "Irregular Periods", "Pregnancy Checkup"], "medicines": ["Folic Acid", "Iron Supplements", "Progesterone"] },
        "Radiology": { "symptoms": ["Injury", "Chest Pain", "Fracture"], "medicines": ["Contrast Dye", "Pain Relief"] },
        "Emergency": { "symptoms": ["Chest Pain", "Accident", "Breathing Difficulty"], "medicines": ["Morphine", "Epinephrine", "Saline"] },
        "Critical Care": { "symptoms": ["Unconscious", "Low BP", "Respiratory Failure"], "medicines": ["Norepinephrine", "Sedatives", "Antibiotics IV"] },
        "Dermatology": { "symptoms": ["Rash", "Itching", "Acne", "Hair Loss"], "medicines": ["Clotrimazole", "Benzoyl Peroxide", "Biotin"] },
        "Psychiatry": { "symptoms": ["Anxiety", "Depression", "Insomnia", "Panic Attack"], "medicines": ["Sertraline", "Escitalopram", "Alprazolam"] },
        "Nephrology": { "symptoms": ["Swelling", "Decreased Urination", "Flank Pain"], "medicines": ["Furosemide", "Erythropoietin"] },
        "Urology": { "symptoms": ["Painful Urination", "Kidney Stones", "Frequency"], "medicines": ["Tamsulosin", "Ciprofloxacin"] },
        "Pulmonology": { "symptoms": ["Wheezing", "Shortness of breath", "Chronic Cough"], "medicines": ["Salbutamol", "Budenoside"] },
        "Endocrinology": { "symptoms": ["Weight Gain", "Excessive Thirst", "Fatigue"], "medicines": ["Metformin", "Levothyroxine"] },
        "Ophthalmology": { "symptoms": ["Blurred Vision", "Eye Redness", "Dry Eyes"], "medicines": ["Carboxymethylcellulose", "Ofloxacin"] },
        "Dental": { "symptoms": ["Toothache", "Gum Swelling", "Sensitivity"], "medicines": ["Amoxicillin", "Paracetamol"] },
        "General Medicine": { "symptoms": ["Fever", "Cough", "Body Ache"], "medicines": ["Paracetamol", "Azithromycin"] },
        "General Surgery": { "symptoms": ["Hernia", "Appendicitis Pain", "Abscess"], "medicines": ["Cefixime", "Tramadol"] },
        "Pathology": { "symptoms": ["Routine Checkup", "Anemia Symptoms"], "medicines": ["Iron Supplements"] },
        "Anaesthesiology": { "symptoms": ["Pre-op Evaluation", "Chronic Pain"], "medicines": ["Gabapentin", "Pregabalin"] }
    }
    DEFAULT_DATA = { "symptoms": ["Fever", "Pain"], "medicines": ["Paracetamol"] }

    case_types = ["Normal", "Emergency", "Critical"]
    
    # Flatten doctors for weighting
    all_docs_flat = []
    for dept, docs in doctors_map.items():
        for staff_id, name in docs:
            # Weighted logic: Cardiology/Orthopaedics get more visits
            multiplier = 4 if dept in ["Cardiology", "Orthopaedics", "Child Care (Paediatrics)"] else 1
            all_docs_flat.extend([(staff_id, dept)] * multiplier)

    new_visits = []
    
    # Generate batch
    for _ in range(NUM_VISITS):
        pid = random.choice(existing_pids)
        staff_id, dept = random.choice(all_docs_flat)
        
        dept_info = DEPT_DATA.get(dept, DEFAULT_DATA)
        
        ctype = random.choices(case_types, weights=[0.80, 0.15, 0.05])[0]
        vdate = get_random_date_between(START_DATE_2024, TARGET_END_DATE, dept)
        
        # Clinical Details
        syms = ", ".join(random.sample(dept_info["symptoms"], k=min(2, len(dept_info["symptoms"]))))
        meds = ", ".join(random.sample(dept_info["medicines"], k=min(2, len(dept_info["medicines"]))))
        
        new_visits.append([pid, dept, staff_id, ctype, vdate.isoformat(), meds, syms])

    # Sort
    print("Sorting visits by date...")
    new_visits.sort(key=lambda x: x[4])

    print(f"Writing to {VISITS_CSV}...")
    with open(VISITS_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['patient_id', 'department', 'doctor', 'case_type', 'visit_date', 'medicines', 'symptoms'])
        writer.writerows(new_visits)

    print("✅ Successfully generated scaled dataset.")

if __name__ == "__main__":
    generate_data()
