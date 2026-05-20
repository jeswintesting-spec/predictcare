import os
import django
from collections import defaultdict
import math

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Department, Doctor, Nurse

DAYS_OF_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def calculate_gini(counts):
    """Calculate Gini Coefficient for a list of values"""
    if not counts:
        return 0.0
    n = len(counts)
    if n == 1:
        return 0.0
    
    # Sort the counts
    x = sorted(counts)
    
    # Calculate Mean
    mean_x = sum(x) / n
    if mean_x == 0:
        return 0.0
    
    # Gini formula
    sum_abs_diff = sum(abs(xi - xj) for xi in x for xj in x)
    gini = sum_abs_diff / (2 * n * n * mean_x)
    return gini

def verify_equity():
    depts = Department.objects.all()
    
    print(f"{'Department':<30} | {'Role':<10} | {'Staff Count':<12} | {'Gini Coeff'}")
    print("-" * 75)
    
    for dept in depts:
        # --- Doctors ---
        docs = Doctor.objects.filter(department=dept)
        if docs.exists():
            doc_counts = []
            for doc in docs:
                # Number of days worked in a week
                days = doc.work_days.split(',')
                doc_counts.append(len(days))
            
            gini = calculate_gini(doc_counts)
            print(f"{dept.name:<30} | {'Doctor':<10} | {docs.count():<12} | {gini:.4f}")
            
        # --- Nurses ---
        nrs = Nurse.objects.filter(department=dept)
        if nrs.exists():
            nrs_counts = []
            for nurse in nrs:
                days = nurse.work_days.split(',')
                nrs_counts.append(len(days))
            
            gini = calculate_gini(nrs_counts)
            print(f"{dept.name:<30} | {'Nurse':<10} | {nrs.count():<12} | {gini:.4f}")

if __name__ == "__main__":
    verify_equity()
