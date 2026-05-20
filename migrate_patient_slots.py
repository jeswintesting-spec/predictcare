import csv
import os

PATIENTS_FILE = 'patients.csv'

def migrate():
    if not os.path.exists(PATIENTS_FILE):
        print("No patients.csv found.")
        return

    print("--- Migrating Patients Schema ---")
    
    with open(PATIENTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
        
    if "assigned_slot" in fieldnames:
        print("✅ 'assigned_slot' column already exists.")
        return

    fieldnames.append("assigned_slot")
    
    with open(PATIENTS_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row['assigned_slot'] = "" # Initialize empty
            writer.writerow(row)
            
    print(f"✅ Added 'assigned_slot' column to {len(rows)} patient records.")

if __name__ == "__main__":
    migrate()
