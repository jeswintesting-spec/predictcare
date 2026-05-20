
import csv
import random

# Kerala Names
first_names_male = ["Rahul", "Arjun", "Vishal", "Sanjay", "Kiran", "Nithin", "Abhilash", "Jitin", "Pranav", "Midhun", "Faisal", "Mohammed", "Aneesh", "Thomas", "Jacob", "Mathew", "George", "Varghese", "Antony", "Sebastian", "Manu", "Vineeth", "Deepak", "Rohan", "Siddharth"]
first_names_female = ["Anjali", "Sreelekshmi", "Meera", "Reshma", "Anupama", "Sneha", "Kavya", "Aiswarya", "Dhanya", "Remya", "Fathima", "Sumayya", "Mary", "Ann", "Sherly", "Leelamma", "Mariamma", "Sophy", "Tessa", "Riya", "Greeshma", "Aswathy", "Lakshmi", "Devika", "Parvathy"]
last_names = ["Nair", "Menon", "Pillai", "Kurup", "Panicker", "Nambiar", "Warrier", "Thampi", "Varghese", "Kurian", "Chacko", "Joseph", "Abraham", "Philip", "George", "Faisal", "Hashim", "Ibrahim", "Siddique", "Rahman", "Mathew", "Cherian", "Eapen", "Samuel", "Thomas"]

departments = [
    "Cardiology", "Child Care (Paediatrics)", "Critical Care", "Emergency", "ENT", 
    "Gastroenterology", "Neurosciences", "Oncology", "Orthopaedics", "Radiology", 
    "Women's Care (Obstetrics & Gynaecology)", "Dermatology", "Psychiatry", "Nephrology", 
    "Urology", "Pulmonology", "Endocrinology", "Ophthalmology", "Dental", 
    "General Medicine", "General Surgery", "Pathology", "Anaesthesiology"
]

def generate_staff():
    # Generate 400 Doctors
    doctors = []
    for i in range(1, 401):
        dept = random.choice(departments)
        gender = random.choice(["Male", "Female"])
        fname = random.choice(first_names_male if gender == "Male" else first_names_female)
        lname = random.choice(last_names)
        name = f"Dr. {fname} {lname}"
        staff_id = f"DOC{i:03d}"
        email = f"dr{fname.lower()}{lname.lower()}@bmh.com"
        phone = f"+91 {random.randint(7000000000, 9999999999)}"
        qual = "MBBS, MD" if random.random() > 0.3 else "MBBS, MS"
        if dept in ["Cardiology", "Neurosciences", "Gastroenterology", "Nephrology", "Oncology"]:
            qual += ", DM" if "MD" in qual else ", MCh"
        
        doctors.append([
            staff_id, dept, name, gender, qual, email, phone, 
            dept, "09:00", "17:00", "Mon,Tue,Wed,Thu,Fri", "Morning", 15, 30
        ])
    
    with open('doctors.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["staff_id","department","doctor_name","gender","qualifications","email","phone","specialization","shift_start","shift_end","work_days","shift_type","slot_duration","max_patients"])
        writer.writerows(doctors)

    # Generate 600 Nurses
    nurses = []
    for i in range(1, 601):
        dept = random.choice(departments)
        gender = random.choice(["Male", "Female"])
        fname = random.choice(first_names_male if gender == "Male" else first_names_female)
        lname = random.choice(last_names)
        name = f"Nurse {fname} {lname}"
        staff_id = f"NUR{i:03d}"
        email = f"nurse{fname.lower()}{lname.lower()}@bmh.com"
        phone = f"+91 {random.randint(7000000000, 9999999999)}"
        
        nurses.append([
            staff_id, dept, name, gender, "B.Sc Nursing", email, phone, 
            "07:00", "15:00", "Mon,Tue,Wed,Thu,Fri", "Morning"
        ])
    
    with open('nurses.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["staff_id","department","nurse_name","gender","qualifications","email","phone","shift_start","shift_end","work_days","shift_type"])
        writer.writerows(nurses)

if __name__ == "__main__":
    generate_staff()
