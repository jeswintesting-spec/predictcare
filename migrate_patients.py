
import csv
import os
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATIENTS_CSV = os.path.join(BASE_DIR, "patients.csv")

KERALA_LOCATIONS = [
    "Thiruvananthapuram, Kerala", "Kochi, Kerala", "Kozhikode, Kerala",
    "Thrissur, Kerala", "Kannur, Kerala", "Kollam, Kerala",
    "Alappuzha, Kerala", "Palakkad, Kerala", "Malappuram, Kerala",
    "Kottayam, Kerala", "Kasaragod, Kerala", "Idukki, Kerala",
    "Wayanad, Kerala", "Pathanamthitta, Kerala"
]

def get_dob_from_age(age):
    try:
        age = int(age)
    except ValueError:
        return ""
    
    today = datetime.now()
    birth_year = today.year - age
    # Random date in that year
    start_date = datetime(birth_year, 1, 1)
    end_date = datetime(birth_year, 12, 31)
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    
    return random_date.strftime("%Y-%m-%d")

def migrate_patients():
    if not os.path.exists(PATIENTS_CSV):
        print("patients.csv not found.")
        return

    updated_rows = []
    
    with open(PATIENTS_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        # Check if already migrated
        if "dob" in fieldnames:
            print("Patients already have DOB/Gender/Location data.")
            return

        # Prepare new headers
        new_headers = list(fieldnames)
        for field in ["dob", "gender", "location"]:
            if field not in new_headers:
                new_headers.append(field)

        for row in reader:
            age = row.get("age", "")
            
            # Generate new data
            if not row.get("dob"):
                row["dob"] = get_dob_from_age(age)
            
            if not row.get("gender"):
                row["gender"] = random.choice(["Male", "Female"])
            
            if not row.get("location"):
                row["location"] = random.choice(KERALA_LOCATIONS)
                
            updated_rows.append(row)

    # Write back
    with open(PATIENTS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_headers)
        writer.writeheader()
        writer.writerows(updated_rows)
    print("Patient details migration complete.")

if __name__ == "__main__":
    migrate_patients()
