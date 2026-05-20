import csv

DOCTORS_FILE = 'doctors.csv'

def update_slots():
    print("--- Updating Doctor Slots ---")
    
    with open(DOCTORS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
        
    for row in rows:
        row['max_patients'] = "25"
        
    with open(DOCTORS_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"✅ Updated {len(rows)} doctors to Max Slots = 25")

if __name__ == "__main__":
    update_slots()
