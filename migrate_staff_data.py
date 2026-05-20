
import csv
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCTORS_CSV = os.path.join(BASE_DIR, "doctors.csv")
NURSES_CSV = os.path.join(BASE_DIR, "nurses.csv")

def generate_email(name):
    clean_name = "".join(e for e in name.lower() if e.isalnum())
    return f"{clean_name}@bmh.com"

def generate_phone():
    return f"+91 {random.randint(6000000000, 9999999999)}"

def migrate_doctors():
    if not os.path.exists(DOCTORS_CSV):
        print("doctors.csv not found.")
        return

    updated_rows = []
    headers = ["staff_id", "department", "doctor_name", "gender", "qualifications", "email", "phone"]
    
    with open(DOCTORS_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Check if already migrated
        if "email" in reader.fieldnames:
            print("Doctors already migrated.")
            return

        for row in reader:
            name = row["doctor_name"]
            row["gender"] = random.choice(["Male", "Female"])
            row["qualifications"] = "MBBS, MD"
            row["email"] = generate_email(name)
            row["phone"] = generate_phone()
            updated_rows.append(row)

    with open(DOCTORS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)
    print("Doctors migrated.")

def migrate_nurses():
    if not os.path.exists(NURSES_CSV):
        print("nurses.csv not found.")
        return

    updated_rows = []
    headers = ["staff_id", "department", "nurse_name", "gender", "qualifications", "email", "phone"]
    
    with open(NURSES_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "email" in reader.fieldnames:
            print("Nurses already migrated.")
            return

        for row in reader:
            name = row["nurse_name"]
            row["gender"] = random.choice(["Male", "Female"])
            row["qualifications"] = "B.Sc Nursing"
            row["email"] = generate_email(name)
            row["phone"] = generate_phone()
            updated_rows.append(row)

    with open(NURSES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)
    print("Nurses migrated.")

if __name__ == "__main__":
    migrate_doctors()
    migrate_nurses()
