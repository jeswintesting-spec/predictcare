
import os
import django
import pandas as pd
from django.conf import settings
from ml.predict_load import analyze_staffing, predict_medicine_demand

# Mock Django settings if needed, or just run purely on CSVs if functions are pure
# The functions in ml/predict_load.py take CSV paths, so they are independent of Django!
# We just need to point to the right files.

BASE = os.getcwd()
VISITS = os.path.join(BASE, "visits.csv")
DOCTORS = os.path.join(BASE, "doctors.csv")
NURSES = os.path.join(BASE, "nurses.csv")

print(f"Checking files:\nVisits: {VISITS}\nDoctors: {DOCTORS}\nNurses: {NURSES}")

if not os.path.exists(VISITS):
    print("ERROR: visits.csv not found")
else:
    print("visits.csv exists.")

try:
    print("--- Running Analysis ---")
    staffing_data = analyze_staffing(VISITS, DOCTORS, NURSES)
    print("Staffing Data Keys:", list(staffing_data.keys()))
    if staffing_data:
        first_dept = list(staffing_data.keys())[0]
        print(f"Sample Dept ({first_dept}):", staffing_data[first_dept])
    else:
        print("Staffing Data is EMPTY!")

    print("\n--- Running Medicine Prediction ---")
    med_data = predict_medicine_demand(VISITS)
    print("Medicine Info:", med_data)
except Exception as e:
    print(f"CRASHED: {e}")
