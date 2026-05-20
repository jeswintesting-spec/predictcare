import csv
import os
import shutil

DOCTORS = "doctors.csv"
NURSES = "nurses.csv"

def migrate_file(filepath, role):
    print(f"Migrating {filepath}...")
    temp_file = filepath + ".tmp"
    
    new_cols = []
    if role == "Doctor":
        new_cols = ["shift_type", "slot_duration", "max_patients"]
    else:
        new_cols = ["shift_type"]

    with open(filepath, "r", encoding="utf-8") as fin, \
         open(temp_file, "w", newline="", encoding="utf-8") as fout:
        
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames
        
        # Add new columns if missing
        for col in new_cols:
            if col not in fieldnames:
                fieldnames.append(col)
        
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            if role == "Doctor":
                if "shift_type" not in row or not row["shift_type"]:
                    row["shift_type"] = "Morning"
                if "slot_duration" not in row or not row["slot_duration"]:
                    row["slot_duration"] = "15"
                if "max_patients" not in row: # Optional
                    row["max_patients"] = ""
            
            if role == "Nurse":
                if "shift_type" not in row or not row["shift_type"]:
                     row["shift_type"] = "Morning"

            writer.writerow(row)
            
    shutil.move(temp_file, filepath)
    print(f"✅ Migrated {filepath}")

if __name__ == "__main__":
    if os.path.exists(DOCTORS): migrate_file(DOCTORS, "Doctor")
    if os.path.exists(NURSES): migrate_file(NURSES, "Nurse")
