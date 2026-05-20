
import os
import random
import datetime
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from pharmacy.models import Medicine

MEDICINE_LIST = {
    # General / Pain
    "Paracetamol 500mg": 25.00,
    "Paracetamol 650mg": 30.00,
    "Ibuprofen 400mg": 45.00,
    "Aspirin 75mg": 15.00,
    "Tramadol 50mg": 120.00,
    "Morphine Injection": 500.00,
    "Diclofenac Gel": 85.00,
    
    # Antibiotics
    "Amoxicillin 500mg": 60.00,
    "Azithromycin 500mg": 110.00,
    "Ciprofloxacin 500mg": 55.00,
    "Metronidazole 400mg": 20.00,
    "Antibiotics IV": 800.00,
    
    # Cardiac / BP
    "Amlodipine 5mg": 35.00,
    "Atorvastatin 10mg": 90.00,
    "Metoprolol 50mg": 45.00,
    "Losartan 50mg": 55.00,
    "Digoxin 0.25mg": 30.00,
    "Norepinephrine Injection": 650.00,
    
    # Gastro
    "Omeprazole 20mg": 40.00,
    "Pantoprazole 40mg": 45.00,
    "Ranitidine 150mg": 18.00,
    "Domperidone 10mg": 25.00,
    "Ondansetron 4mg": 35.00,
    
    # Neuro / Psych
    "Gabapentin 300mg": 110.00,
    "Levetiracetam 500mg": 150.00,
    "Sertraline 50mg": 85.00,
    "Diazepam 5mg": 40.00,
    
    # Diabetes / Endocrine
    "Metformin 500mg": 22.00,
    "Glimepiride 1mg": 30.00,
    "Insulin Glargine": 1200.00,
    "Thyroxine 50mcg": 120.00,
    
    # Respiratory / ENT
    "Cetirizine 10mg": 20.00,
    "Montelukast 10mg": 70.00,
    "Salbutamol Inhaler": 250.00,
    "Nasal Spray (Xylometazoline)": 90.00,
    "Cough Syrup": 120.00,
    
    # Vitamins / Supplements
    "Vitamin D3 60k": 150.00,
    "Calcium + Vit D3": 180.00,
    "Iron Folic Acid": 80.00,
    "Multivitamin Tablets": 110.00,
    "B-Complex Injection": 40.00,
    
    # Emergency / Other
    "Saline IV 500ml": 100.00,
    "Epinephrine Injection": 300.00,
    "Contrast Dye": 1500.00,
    "Progesterone 200mg": 350.00
}

def seed_inventory():
    print("Seeding Pharmacy Inventory...")
    count = 0
    for name, price in MEDICINE_LIST.items():
        # EXPIRY in 1-2 years
        expiry = datetime.date.today() + datetime.timedelta(days=random.randint(365, 730))
        
        # Check if exists
        if not Medicine.objects.filter(name=name).exists():
            Medicine.objects.create(
                name=name,
                price=price,
                stock_quantity=random.randint(500, 2000),
                min_stock_level=100,
                expiry_date=expiry
            )
            print(f"Added: {name}")
            count += 1
        else:
            print(f"Skipped: {name} (Already exists)")
            
    print(f"Done. Added {count} new medicines.")

if __name__ == "__main__":
    seed_inventory()
