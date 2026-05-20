import csv
import os

VISITS_FILE = 'visits.csv'

def migrate_visits():
    if not os.path.exists(VISITS_FILE):
        print("No visits.csv found.")
        return

    print("--- Migrating Visits Schema ---")
    
    with open(VISITS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
        
    if "slot" in fieldnames:
        print("✅ 'slot' column already exists.")
        return

    fieldnames.append("slot")
    
    with open(VISITS_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row['slot'] = "" # Initialize empty
            writer.writerow(row)
            
    print(f"✅ Added 'slot' column to {len(rows)} visit records.")

if __name__ == "__main__":
    migrate_visits()
