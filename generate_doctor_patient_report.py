import csv
from collections import defaultdict
from datetime import datetime

# Read visits data
visits_data = []
with open('visits.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        visits_data.append(row)

# Organize data by date, department, and doctor
report_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

for visit in visits_data:
    date = visit['visit_date']
    department = visit['department']
    doctor = visit['doctor']
    
    # Count patients per doctor per department per date
    report_data[date][department][doctor] += 1

# Prepare CSV output
output_file = 'doctor_patient_report.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow(['Date', 'Department', 'Doctor', 'Number of Patients'])
    
    # Sort dates
    sorted_dates = sorted(report_data.keys())
    
    # Write data with subtotals
    for date in sorted_dates:
        date_total = 0
        
        for department in sorted(report_data[date].keys()):
            dept_total = 0
            
            for doctor in sorted(report_data[date][department].keys()):
                patient_count = report_data[date][department][doctor]
                writer.writerow([date, department, doctor, patient_count])
                dept_total += patient_count
                date_total += patient_count
            
            # Department subtotal
            writer.writerow([date, department, 'DEPARTMENT TOTAL', dept_total])
        
        # Date total
        writer.writerow([date, 'DATE TOTAL', '', date_total])
        writer.writerow([])  # Empty row for readability

# Calculate and add grand totals
grand_total_by_department = defaultdict(int)
grand_total_by_doctor = defaultdict(int)
overall_total = 0

for date in report_data:
    for department in report_data[date]:
        for doctor in report_data[date][department]:
            count = report_data[date][department][doctor]
            grand_total_by_department[department] += count
            grand_total_by_doctor[doctor] += count
            overall_total += count

# Append summary section
with open(output_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    writer.writerow([])
    writer.writerow(['SUMMARY BY DEPARTMENT'])
    writer.writerow(['Department', 'Total Patients'])
    for dept in sorted(grand_total_by_department.keys()):
        writer.writerow([dept, grand_total_by_department[dept]])
    
    writer.writerow([])
    writer.writerow(['SUMMARY BY DOCTOR'])
    writer.writerow(['Doctor', 'Total Patients'])
    for doctor in sorted(grand_total_by_doctor.keys()):
        writer.writerow([doctor, grand_total_by_doctor[doctor]])
    
    writer.writerow([])
    writer.writerow(['GRAND TOTAL', overall_total])

print(f"Report generated successfully: {output_file}")
print(f"Total visits processed: {overall_total}")
print(f"Date range: {min(sorted_dates)} to {max(sorted_dates)}")
