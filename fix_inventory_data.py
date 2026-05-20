
import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from pharmacy.models import Medicine

def fix_inventory():
    print("Fixing Inventory Data for 'Perfect' Alerts...")
    
    medicines = list(Medicine.objects.all())
    if not medicines:
        print("No medicines found.")
        return

    # Randomly select 5-8 medicines to be LOW STOCK
    low_stock_target = random.sample(medicines, min(len(medicines), random.randint(5, 8)))
    
    for med in low_stock_target:
        # Set stock below min_stock_level
        med.stock_quantity = random.randint(0, med.min_stock_level - 1)
        med.save()
        print(f"Low Stock Set: {med.name} (Stock: {med.stock_quantity}, Min: {med.min_stock_level})")

    # Ensure some medicines are WELL STOCKED
    other_meds = [m for m in medicines if m not in low_stock_target]
    for med in other_meds[:10]:
        med.stock_quantity = random.randint(med.min_stock_level + 200, 500)
        med.save()

    print("Done. Inventory health adjusted.")

if __name__ == "__main__":
    fix_inventory()
