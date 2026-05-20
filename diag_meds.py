import os
import django
import pandas as pd
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Visit
from ml.predict_load import predict_medicine_demand_from_df

def run_diagnostic():
    print("Fetching visits...")
    visits_qs = Visit.objects.all().order_by('-visit_date')[:100000].values('visit_date', 'medicines')
    df = pd.DataFrame(list(visits_qs))
    
    print(f"Total visits fetched: {len(df)}")
    if df.empty:
        print("No visits found!")
        return

    print("Running prediction...")
    # Simulate the call in views.py (except we already sampled here for speed)
    forecast = predict_medicine_demand_from_df(df)
    
    print("\nForecast Results (Top 10):")
    print(json.dumps(forecast, indent=2))
    
    # Internal check of the steps
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors='coerce')
    df = df.dropna(subset=["visit_date"])
    df["month_index"] = df["visit_date"].dt.year * 12 + df["visit_date"].dt.month
    
    print(f"\nMonth indices in sample: {df['month_index'].unique()}")
    
    med_series = df.set_index('month_index')['medicines'].str.split(',')
    med_series = med_series.explode().str.strip()
    med_series = med_series[med_series != '']
    
    if med_series.empty:
        print("No medicines found in sample!")
        return
        
    med_counts = med_series.reset_index().groupby(['medicines', 'month_index']).size().reset_index(name='count')
    print(f"Medicine counts sample:\n{med_counts.head()}")

if __name__ == "__main__":
    run_diagnostic()
