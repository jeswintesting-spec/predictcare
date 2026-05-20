
import csv
import os

PATIENTS = "patients.csv"
VISITS = "visits.csv"

def prune_visits():
    # 1. Load valid Patient IDs
    valid_ids = set()
    if os.path.exists(PATIENTS):
        with open(PATIENTS, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if row and len(row) > 0:
                    valid_ids.add(row[0].strip().upper())
    
    print(f"Loaded {len(valid_ids)} valid patient IDs.")

    # 2. Filter Visits
    kept = []
    removed_count = 0
    header = []

    if os.path.exists(VISITS):
        with open(VISITS, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            kept.append(header)
            
            for row in reader:
                if row and len(row) > 0:
                    pid = row[0].strip().upper()
                    if pid in valid_ids:
                        kept.append(row)
                    else:
                        removed_count += 1
    
    # 3. Write back
    with open(VISITS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(kept)

    print(f"Pruned visits.csv: Kept {len(kept)-1}, Removed {removed_count} orphan visits.")

if __name__ == "__main__":
    prune_visits()
