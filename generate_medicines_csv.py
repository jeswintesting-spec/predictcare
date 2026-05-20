
import csv
import random
import datetime

# This list matches exactly what is used in generate_real_data_2026.py
MEDICINE_DATA = {
    "Amlodipine": 35.00, "Atorvastatin": 90.00, "Aspirin": 15.00, "Metoprolol": 45.00,
    "Omeprazole": 40.00, "Pantoprazole": 45.00, "Metformin": 22.00, "Ranitidine": 18.00,
    "Gabapentin": 110.00, "Topiramate": 125.00, "Levetiracetam": 150.00,
    "Ibuprofen": 45.00, "Paracetamol": 25.00, "Calcium": 65.00, "Vitamin D3": 120.00,
    "Paracetamol Syrup": 40.00, "Amoxicillin": 60.00, "Ibuprofen Syrup": 50.00,
    "Cetirizine": 20.00, "Nasal Spray": 90.00,
    "Tramadol": 120.00, "Morphine": 500.00, "Ondansetron": 35.00,
    "Folic Acid": 80.00, "Iron Supplements": 90.00, "Progesterone": 350.00,
    "Contrast Dye": 1500.00, "Pain Relief": 85.00,
    "Epinephrine": 300.00, "Saline": 100.00,
    "Norepinephrine": 650.00, "Sedatives": 400.00, "Antibiotics IV": 800.00,
    "Clotrimazole": 85.00, "Benzoyl Peroxide": 220.00, "Biotin": 180.00,
    "Sertraline": 85.00, "Escitalopram": 95.00, "Alprazolam": 45.00,
    "Furosemide": 40.00, "Erythropoietin": 1100.00,
    "Tamsulosin": 120.00, "Ciprofloxacin": 55.00,
    "Salbutamol": 250.00, "Budenoside": 450.00,
    "Levothyroxine": 120.00,
    "Carboxymethylcellulose": 110.00, "Ofloxacin": 65.00,
    "Azithromycin": 110.00,
    "Cefixime": 130.00,
    "Pregabalin": 180.00
}

def generate_medicines_csv():
    print("Generating medicines.csv...")
    filename = "medicines.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'price', 'stock_quantity', 'min_stock_level', 'expiry_date'])
        
        for name, price in MEDICINE_DATA.items():
            stock = random.randint(500, 2000)
            min_level = 100
            # Expiry 1-3 years out
            expiry = (datetime.date.today() + datetime.timedelta(days=random.randint(365, 1095))).isoformat()
            writer.writerow([name, price, stock, min_level, expiry])
            
    print(f"✅ Successfully created {filename} with {len(MEDICINE_DATA)} items.")

if __name__ == "__main__":
    generate_medicines_csv()
