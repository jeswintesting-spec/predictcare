
import os
import random
import datetime
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from pharmacy.models import Medicine

# Lists to generate unique medicine names
ROOTS = [
    "Amlodip", "Atorvast", "Metform", "Amoxicil", "Azithrom", "Ciproflox", "Metronid",
    "Omepraz", "Pantopraz", "Ranitid", "Lisinopr", "Losart", "Simvast", "Gabapent",
    "Sertral", "Levothyr", "Furosem", "Alprazol", "Clonazep", "Warfar", "Clopidog",
    "Prednis", "Monteluk", "Salbutam", "Tamsulos", "Duloxet", "Escitalop", "Venlafax",
    "Bupropi", "Rosuvast", "Valsart", "Ondanset", "Meloxic", "Tramad", "Pregabal",
    "Zolpid", "Warfar", "Aspir", "Naprox", "Celecox", "Clarithrom", "Levoflox", "Doxycycl",
    "Fluconaz", "Valacycl", "Acyclov", "Venlafax", "Duloxet", "Paroxet", "Fluoxe", "Citalop"
]

POTENCIES = ["2.5mg", "5mg", "10mg", "20mg", "25mg", "40mg", "50mg", "100mg", "150mg", "200mg", "250mg", "300mg", "400mg", "500mg", "600mg", "625mg", "750mg", "800mg", "1000mg"]
FORMS = ["Tablet", "Capsule", "Injection", "Syrup", "Gel", "Ointment", "Cream", "Sachet", "Inhaler", "Suspension", "Vial"]

def generate_medicines(count=210):
    print(f"Generating {count} new medicines...")
    added_count = 0
    skipped_count = 0
    
    unique_names = set()
    while len(unique_names) < count:
        root = random.choice(ROOTS)
        potency = random.choice(POTENCIES)
        form = random.choice(FORMS)
        name = f"{root} {potency} {form}"
        unique_names.add(name)

    for name in unique_names:
        # Check if already exists
        if Medicine.objects.filter(name=name).exists():
            skipped_count += 1
            continue
            
        price = round(random.uniform(15.00, 2500.00), 2)
        stock = random.randint(1000, 5000)
        min_level = random.choice([50, 100, 200])
        expiry = datetime.date.today() + datetime.timedelta(days=random.randint(365, 1095)) # 1-3 years
        
        Medicine.objects.create(
            name=name,
            price=price,
            stock_quantity=stock,
            min_stock_level=min_level,
            expiry_date=expiry
        )
        added_count += 1
        if added_count % 50 == 0:
            print(f"Progress: Added {added_count} medicines...")

    print(f"\nFinal Result:")
    print(f"Successfully added: {added_count}")
    print(f"Skipped (already exists): {skipped_count}")
    print(f"Total inventory size: {Medicine.objects.count()}")

if __name__ == "__main__":
    generate_medicines(210)
