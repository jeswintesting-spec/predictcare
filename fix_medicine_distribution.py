import os
import django
import random
from collections import Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Visit
from django.core.cache import cache

def fix_distribution():
    print("Fixing medicine distribution for the latest 10,000 visits to make charts look beautiful...")
    
    # Let's create a weighted list of medicines for a smooth, realistic downward curve in the chart
    top_tier = ["Atorvastatin", "Metformin", "Amlodipine", "Levothyroxine", "Omeprazole", "Losartan"] # Very common
    mid_tier = ["Azithromycin", "Amoxicillin", "Pantoprazole", "Gabapentin", "Sertraline", "Ibuprofen", "Aspirin", "Paracetamol", "Montelukast"] # Common
    low_tier = ["Ciprofloxacin", "Metronidazole", "Ranitidine", "Simvastatin", "Furosemide", "Alprazolam", "Clonazepam", "Clopidogrel", "Prednisone", "Salbutamol"] # Less common
    rare_tier = ["Tamsulosin", "Duloxetine", "Escitalopram", "Venlafaxine", "Bupropion", "Rosuvastatin", "Valsartan", "Ondansetron", "Meloxicam", "Tramadol", "Pregabalin", "Zolpidem", "Naproxen", "Celecoxib", "Fluconazole", "Acyclovir"]
    
    # Give them weights so top_tier gets picked most often, creating a realistic curve
    all_meds = []
    # 35% top, 35% mid, 20% low, 10% rare
    for m in top_tier: all_meds.extend([m] * 300)
    for m in mid_tier: all_meds.extend([m] * 150)
    for m in low_tier: all_meds.extend([m] * 50)
    for m in rare_tier: all_meds.extend([m] * 15)

    recent_visits = list(Visit.objects.all().order_by('-visit_date')[:10000])
    
    updates = []
    for v in recent_visits:
        # Give each visit 1 to 3 medicines based on our weighted distribution
        num_meds = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
        
        # Sample without replacement for a single visit
        chosen_meds = set()
        while len(chosen_meds) < num_meds:
            chosen_meds.add(random.choice(all_meds))
            
        v.medicines = ", ".join(list(chosen_meds))
        updates.append(v)
        
    # Bulk update to be fast
    Visit.objects.bulk_update(updates, ['medicines'])
    
    # Clear the caching to ensure graphs update immediately
    cache.delete('hospital_analytics_data')
    print(f"Successfully redistributed medicines for {len(updates)} visits for presentation.")

if __name__ == '__main__':
    fix_distribution()
