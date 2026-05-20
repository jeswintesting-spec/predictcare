import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Visit

DEPT_DATA = {
        "Cardiology": { "symptoms": ["Chest Pain", "Palpitations", "Shortness of breath", "Dizziness", "Fatigue"], "medicines": ["Amlodipine", "Atorvastatin", "Aspirin", "Metoprolol"] },
        "Gastroenterology": { "symptoms": ["Abdominal Pain", "Nausea", "Vomiting", "Heartburn"], "medicines": ["Omeprazole", "Pantoprazole", "Metformin", "Ranitidine"] },
        "Neurosciences": { "symptoms": ["Headache", "Seizures", "Migraine", "Dizziness"], "medicines": ["Gabapentin", "Topiramate", "Levetiracetam"] },
        "Orthopaedics": { "symptoms": ["Joint Pain", "Back Pain", "Fracture", "Muscle Pain"], "medicines": ["Ibuprofen", "Paracetamol", "Calcium", "Vitamin D3"] },
        "Child Care (Paediatrics)": { "symptoms": ["Fever", "Cough", "Cold", "Rash"], "medicines": ["Paracetamol Syrup", "Amoxicillin", "Ibuprofen Syrup"] },
        "ENT": { "symptoms": ["Sore Throat", "Ear Pain", "Nasal Congestion"], "medicines": ["Cetirizine", "Nasal Spray", "Amoxicillin"] },
        "Oncology": { "symptoms": ["Fatigue", "Weight Loss", "Lump", "Pain"], "medicines": ["Tramadol", "Morphine", "Ondansetron"] },
        "Women's Care (Obstetrics & Gynaecology)": { "symptoms": ["Cramps", "Irregular Periods", "Pregnancy Checkup"], "medicines": ["Folic Acid", "Iron Supplements", "Progesterone"] },
        "Radiology": { "symptoms": ["Injury", "Chest Pain", "Fracture"], "medicines": ["Contrast Dye", "Pain Relief"] },
        "Emergency": { "symptoms": ["Chest Pain", "Accident", "Breathing Difficulty"], "medicines": ["Morphine", "Epinephrine", "Saline"] },
        "Critical Care": { "symptoms": ["Unconscious", "Low BP", "Respiratory Failure"], "medicines": ["Norepinephrine", "Sedatives", "Antibiotics IV"] },
        "Dermatology": { "symptoms": ["Rash", "Itching", "Acne", "Hair Loss"], "medicines": ["Clotrimazole", "Benzoyl Peroxide", "Biotin"] },
        "Psychiatry": { "symptoms": ["Anxiety", "Depression", "Insomnia", "Panic Attack"], "medicines": ["Sertraline", "Escitalopram", "Alprazolam"] },
        "Nephrology": { "symptoms": ["Swelling", "Decreased Urination", "Flank Pain"], "medicines": ["Furosemide", "Erythropoietin"] },
        "Urology": { "symptoms": ["Painful Urination", "Kidney Stones", "Frequency"], "medicines": ["Tamsulosin", "Ciprofloxacin"] },
        "Pulmonology": { "symptoms": ["Wheezing", "Shortness of breath", "Chronic Cough"], "medicines": ["Salbutamol", "Budenoside"] },
        "Endocrinology": { "symptoms": ["Weight Gain", "Excessive Thirst", "Fatigue"], "medicines": ["Metformin", "Levothyroxine"] },
        "Ophthalmology": { "symptoms": ["Blurred Vision", "Eye Redness", "Dry Eyes"], "medicines": ["Carboxymethylcellulose", "Ofloxacin"] },
        "Dental": { "symptoms": ["Toothache", "Gum Swelling", "Sensitivity"], "medicines": ["Amoxicillin", "Paracetamol"] },
        "General Medicine": { "symptoms": ["Fever", "Cough", "Body Ache"], "medicines": ["Paracetamol", "Azithromycin"] },
        "General Surgery": { "symptoms": ["Hernia", "Appendicitis Pain", "Abscess"], "medicines": ["Cefixime", "Tramadol"] },
        "Pathology": { "symptoms": ["Routine Checkup", "Anemia Symptoms"], "medicines": ["Iron Supplements"] },
        "Anaesthesiology": { "symptoms": ["Pre-op Evaluation", "Chronic Pain"], "medicines": ["Gabapentin", "Pregabalin"] }
}
DEFAULT_DATA = { "symptoms": ["Fever", "Pain"], "medicines": ["Paracetamol"] }

visits_to_fix = Visit.objects.filter(medicines="Paracetamol, Amoxicillin").select_related('department')

count = 0
for v in visits_to_fix:
    dept_name = v.department.name
    dept_info = DEPT_DATA.get(dept_name, DEFAULT_DATA)
    syms = ", ".join(random.sample(dept_info["symptoms"], k=min(2, len(dept_info["symptoms"]))))
    meds = ", ".join(random.sample(dept_info["medicines"], k=min(2, len(dept_info["medicines"]))))
    
    v.symptoms = syms
    v.medicines = meds
    v.save()
    count += 1
    if count % 500 == 0:
        print(f"Fixed {count} visits")

# Clear the cache
from django.core.cache import cache
cache.delete('hospital_analytics_data')

print(f"Done fixing {count} visits.")
