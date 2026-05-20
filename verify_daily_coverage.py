import csv
from collections import defaultdict

def load_csv(filename):
    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

def verify_daily_coverage():
    staff_files = [('doctors.csv', 'Doctor'), ('nurses.csv', 'Nurse')]
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    print("--- Verifying Daily Coverage ---")
    
    for filename, role in staff_files:
        data = load_csv(filename)
        # Structure: Department -> ShiftType -> Day -> Count
        coverage = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        
        for p in data:
            dept = p['department']
            shift = p['shift_type']
            work_days = set(p['work_days'].split(","))
            
            for day in DAYS:
                if day in work_days:
                    coverage[dept][shift][day] += 1
                    
        # Check constraints
        issues = 0
        total_checks = 0
        
        for dept, shifts in coverage.items():
            for shift, days_map in shifts.items():
                for day in DAYS:
                    total_checks += 1
                    count = days_map[day]
                    if count == 0:
                        print(f"❌ {role} GAP: {dept} - {shift} on {day} has 0 staff")
                        issues += 1
                        
        print(f"Checked {total_checks} {role} slots across all depts/shifts/days.")
        
        if issues == 0:
            print(f"✅ {role} coverage is perfect (7 days/week for all shifts)")
        else:
             print(f"⚠️ Found {issues} gaps for {role}")

if __name__ == "__main__":
    verify_daily_coverage()
