import csv
import os
import shutil

DOCTORS = "doctors.csv"
NURSES = "nurses.csv"

def migrate_file(filepath):
    print(f"Migrating {filepath}...")
    temp_file = filepath + ".tmp"
    with open(filepath, "r", encoding="utf-8") as fin, \
         open(temp_file, "w", newline="", encoding="utf-8") as fout:
        
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames
        
        # Add new columns if missing
        new_cols = ["shift_start", "shift_end", "work_days"]
        for col in new_cols:
            if col not in fieldnames:
                fieldnames.append(col)
        
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            if "shift_start" not in row or not row["shift_start"]:
                row["shift_start"] = "09:00"
            if "shift_end" not in row or not row["shift_end"]:
                 row["shift_end"] = "17:00"
            if "work_days" not in row or not row["work_days"]:
                 row["work_days"] = "Mon,Tue,Wed,Thu,Fri"
            writer.writerow(row)
            
    shutil.move(temp_file, filepath)
    print(f"✅ Migrated {filepath}")

if __name__ == "__main__":
    if os.path.exists(DOCTORS): migrate_file(DOCTORS)
    if os.path.exists(NURSES): migrate_file(NURSES)
