
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCTORS_CSV = os.path.join(BASE_DIR, "doctors.csv")

DEPT_MAP = {
    "Cardiology": "Cardiologist",
    "Child Care (Paediatrics)": "Paediatrician",
    "Critical Care": "Intensivist",
    "ENT": "ENT Specialist",
    "Emergency": "Emergency Physician",
    "Gastroenterology": "Gastroenterologist",
    "Neurosciences": "Neurologist",
    "Oncology": "Oncologist",
    "Orthopaedics": "Orthopaedic Surgeon",
    "Radiology": "Radiologist",
    "Women's Care (Obstetrics & Gynaecology)": "Gynecologist"
}

def migrate_doctors_specialization():
    if not os.path.exists(DOCTORS_CSV):
        print("doctors.csv not found.")
        return

    updated_rows = []
    # We read first to check headers
    with open(DOCTORS_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if "specialization" in fieldnames:
            print("Doctors already have specialization field.")
            return

        # Prepare new headers
        new_headers = list(fieldnames) + ["specialization"]

        for row in reader:
            dept = row.get("department", "")
            # Default to General Practitioner if dept mapping not found
            spec = DEPT_MAP.get(dept, "General Practitioner")
            row["specialization"] = spec
            updated_rows.append(row)

    # Write back
    with open(DOCTORS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_headers)
        writer.writeheader()
        writer.writerows(updated_rows)
    print("Doctors specialization migration complete.")

if __name__ == "__main__":
    migrate_doctors_specialization()
