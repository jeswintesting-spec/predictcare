"""
Django management command to migrate CSV data to PostgreSQL database.
Usage: python manage.py migrate_csv_to_db
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from hospital.models import Department, Doctor, Nurse, Patient, Visit
from pharmacy.models import Medicine, PrescriptionLine, PharmacyBill, BillItem
import csv
import os
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Migrate data from CSV files to PostgreSQL database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-visits',
            action='store_true',
            help='Skip importing visits (useful for testing)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing hospital and pharmacy data before migration',
        )

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        self.stdout.write(self.style.SUCCESS('Starting CSV to PostgreSQL migration...'))
        self.stdout.write(f'Base directory: {base_dir}')

        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data with TRUNCATE...'))
            from django.db import connection
            with connection.cursor() as cursor:
                # Truncate all hospital and pharmacy tables and reset sequences
                tables = [
                    'pharmacy_billitem', 'pharmacy_pharmacybill', 'pharmacy_prescriptionline',
                    'pharmacy_medicine', 'hospital_visit', 'hospital_patient',
                    'hospital_doctor', 'hospital_nurse', 'hospital_department'
                ]
                # Filter for existing tables to avoid errors if some are missing
                cursor.execute(f"TRUNCATE TABLE {', '.join(tables)} RESTART IDENTITY CASCADE;")
            self.stdout.write(self.style.SUCCESS('  ✓ Data cleared and sequences reset'))
        
        # 0. Import Medicines (New)
        self.import_medicines(base_dir)

        # 1. Import Departments
        self.import_departments(base_dir)
        
        # 2. Import Doctors
        self.import_doctors(base_dir)
        
        # 3. Import Nurses
        self.import_nurses(base_dir)
        
        # 4. Import Patients
        self.import_patients(base_dir)
        
        # 5. Import Visits
        if not options['skip_visits']:
            self.import_visits(base_dir)
        else:
            self.stdout.write(self.style.WARNING('Skipping visits import'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Migration completed successfully!'))

    def import_medicines(self, base_dir):
        """Import medicines from medicines.csv"""
        csv_path = os.path.join(base_dir, 'medicines.csv')
        self.stdout.write(f'\nImporting medicines from {csv_path}...')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'File not found: {csv_path}'))
            return
        
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Medicine.objects.get_or_create(
                    name=row['name'].strip(),
                    defaults={
                        'price': row['price'],
                        'stock_quantity': row['stock_quantity'],
                        'min_stock_level': row['min_stock_level'],
                        'expiry_date': row['expiry_date']
                    }
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {count} medicines'))
            


    def import_departments(self, base_dir):
        """Import departments from departments.csv"""
        csv_path = os.path.join(base_dir, 'departments.csv')
        self.stdout.write(f'\\nImporting departments from {csv_path}...')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'File not found: {csv_path}'))
            return
        
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name'].strip()
                if name:  # Skip empty lines
                    Department.objects.get_or_create(name=name)
                    count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {count} departments'))

    def import_doctors(self, base_dir):
        """Import doctors from doctors.csv"""
        csv_path = os.path.join(base_dir, 'doctors.csv')
        self.stdout.write(f'\\nImporting doctors from {csv_path}...')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'File not found: {csv_path}'))
            return
        
        count = 0
        errors = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if not row['staff_id'].strip():
                        continue
                    
                    department, _ = Department.objects.get_or_create(name=row['department'])
                    
                    Doctor.objects.get_or_create(
                        staff_id=row['staff_id'],
                        defaults={
                            'department': department,
                            'doctor_name': row['doctor_name'],
                            'gender': row.get('gender', 'Male'),
                            'qualifications': row.get('qualifications', ''),
                            'email': row.get('email', ''),
                            'phone': row.get('phone', ''),
                            'specialization': row.get('specialization', ''),
                            'shift_start': row.get('shift_start', '09:00'),
                            'shift_end': row.get('shift_end', '17:00'),
                            'work_days': row.get('work_days', 'Mon,Tue,Wed,Thu,Fri'),
                            'shift_type': row.get('shift_type', 'Morning'),
                            'slot_duration': int(row.get('slot_duration', 15)),
                            'max_patients': int(row.get('max_patients', 25)),
                        }
                    )
                    count += 1
                except Exception as e:
                    errors += 1
                    self.stdout.write(self.style.WARNING(f'  Error importing doctor {row.get("staff_id")}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {count} doctors ({errors} errors)'))

    def import_nurses(self, base_dir):
        """Import nurses from nurses.csv"""
        csv_path = os.path.join(base_dir, 'nurses.csv')
        self.stdout.write(f'\\nImporting nurses from {csv_path}...')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'File not found: {csv_path}'))
            return
        
        count = 0
        errors = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if not row['staff_id'].strip():
                        continue
                    
                    department, _ = Department.objects.get_or_create(name=row['department'])
                    
                    Nurse.objects.get_or_create(
                        staff_id=row['staff_id'],
                        defaults={
                            'department': department,
                            'nurse_name': row['nurse_name'],
                            'gender': row.get('gender', 'Female'),
                            'qualifications': row.get('qualifications', ''),
                            'email': row.get('email', ''),
                            'phone': row.get('phone', ''),
                            'shift_start': row.get('shift_start', '09:00'),
                            'shift_end': row.get('shift_end', '17:00'),
                            'work_days': row.get('work_days', 'Mon,Tue,Wed,Thu,Fri'),
                            'shift_type': row.get('shift_type', 'Morning'),
                        }
                    )
                    count += 1
                except Exception as e:
                    errors += 1
                    self.stdout.write(self.style.WARNING(f'  Error importing nurse {row.get("staff_id")}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {count} nurses ({errors} errors)'))

    def import_patients(self, base_dir):
        """Import patients from patients.csv"""
        csv_path = os.path.join(base_dir, 'patients.csv')
        self.stdout.write(f'\\nImporting patients from {csv_path}...')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'File not found: {csv_path}'))
            return
        
        # Preload doctors for efficient lookup
        doctors_map = {d.doctor_name: d for d in Doctor.objects.all()}
        
        count = 0
        errors = 0
        batch = []
        batch_size = 1000
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if not row['patient_id'].strip():
                        continue
                    
                    # Parse date of birth
                    dob = None
                    if row.get('dob'):
                        try:
                            dob = datetime.strptime(row['dob'], '%Y-%m-%d').date()
                        except:
                            pass
                    
                    # Lookup doctor
                    doc_name = row.get('doctor', '').strip()
                    doctor_obj = doctors_map.get(doc_name)
                    
                    patient = Patient(
                        patient_id=row['patient_id'],
                        patient_name=row['patient_name'],
                        age=int(row.get('age', 0)),
                        dob=dob,
                        gender=row.get('gender', 'Male'),
                        location=row.get('location', ''),
                        assigned_slot=row.get('assigned_slot', ''),
                        doctor=doctor_obj
                    )
                    batch.append(patient)
                    count += 1
                    
                    # Bulk create in batches for performance
                    if len(batch) >= batch_size:
                        Patient.objects.bulk_create(batch, ignore_conflicts=True)
                        batch = []
                        self.stdout.write(f'  Progress: {count} patients...', ending='\\r')
                        
                except Exception as e:
                    errors += 1
                    if errors < 10:  # Only show first 10 errors
                        self.stdout.write(self.style.WARNING(f'  Error importing patient {row.get("patient_id")}: {str(e)}'))
            
            # Create remaining batch
            if batch:
                Patient.objects.bulk_create(batch, ignore_conflicts=True)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {count} patients ({errors} errors)'))

    def import_visits(self, base_dir):
        """Import visits and link to prescriptions/bills"""
        csv_path = os.path.join(base_dir, 'visits.csv')
        self.stdout.write(f'\nImporting visits and generating prescriptions/bills from {csv_path}...')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'File not found: {csv_path}'))
            return
        
        # Preload for performance
        medicines_map = {m.name: m for m in Medicine.objects.all()}
        patient_cache = {p.patient_id: p for p in Patient.objects.all()}
        doctor_cache = {d.staff_id: d for d in Doctor.objects.all()}
        dept_cache = {dept.name: dept for dept in Department.objects.all()}

        count = 0
        errors = 0
        batch_size = 2000
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch_visits = []
            
            for row in reader:
                try:
                    patient = patient_cache.get(row['patient_id'])
                    department = dept_cache.get(row['department'])
                    doctor = doctor_cache.get(row['doctor'])
                    
                    if not (patient and department and doctor):
                        continue

                    visit_date = datetime.strptime(row['visit_date'], '%Y-%m-%d').date()
                    
                    visit = Visit(
                        patient=patient,
                        department=department,
                        doctor=doctor,
                        case_type=row.get('case_type', 'Normal'),
                        visit_date=visit_date,
                        medicines=row.get('medicines', ''),
                        symptoms=row.get('symptoms', ''),
                        slot=row.get('slot', ''),
                    )
                    batch_visits.append(visit)
                    count += 1
                    
                    if len(batch_visits) >= batch_size:
                        created_visits = Visit.objects.bulk_create(batch_visits)
                        self.process_pharmacy_links(created_visits, medicines_map)
                        batch_visits = []
                        self.stdout.write(f'  Progress: {count} visits...', ending='\r')
                        
                except Exception as e:
                    errors += 1
                    if errors < 10:
                        self.stdout.write(self.style.WARNING(f'  Error importing visit: {str(e)}'))
            
            if batch_visits:
                created_visits = Visit.objects.bulk_create(batch_visits)
                self.process_pharmacy_links(created_visits, medicines_map)
        
        self.stdout.write(self.style.SUCCESS(f'\n  ✓ Imported {count} visits and linked pharmacy data ({errors} errors)'))

    def process_pharmacy_links(self, visits, medicines_map):
        """Helper to create prescriptions and bills for a batch of visits"""
        prescription_lines = []
        bills_to_create = []
        bill_meds_map = [] # stores (bill_obj, [med_objs])
        
        for visit in visits:
            med_names = [m.strip() for m in visit.medicines.split(',') if m.strip()]
            if not med_names:
                continue

            # 1. Create PrescriptionLines
            visit_meds = []
            for mname in med_names:
                med_obj = medicines_map.get(mname)
                if med_obj:
                    visit_meds.append(med_obj)
                    prescription_lines.append(PrescriptionLine(
                        visit=visit,
                        medicine=med_obj,
                        quantity=random.randint(1, 4),
                        dosage_instructions=random.choice(["1-0-1", "1-1-1", "0-0-1", "1-0-0"]) + " after food"
                    ))

            # 2. Randomly create a PharmacyBill for the visit (70% probability)
            if visit_meds and random.random() < 0.7:
                total = sum(m.price * 2 for m in visit_meds) # approx price
                
                # Use visit_date for historical bill date
                # Combine date with midnight time for a valid datetime
                bill_time = datetime.combine(visit.visit_date, datetime.min.time())
                
                bill = PharmacyBill(
                    customer_name=visit.patient.patient_name,
                    patient=visit.patient,
                    total_amount=total,
                    created_at=bill_time
                )
                bills_to_create.append(bill)
                bill_meds_map.append(visit_meds)

        # Bulk create prescriptions
        if prescription_lines:
            PrescriptionLine.objects.bulk_create(prescription_lines)
        
        # Bulk create bills and then their items
        if bills_to_create:
            created_bills = PharmacyBill.objects.bulk_create(bills_to_create)
            
            bill_items = []
            for i, bill in enumerate(created_bills):
                meds = bill_meds_map[i]
                for med in meds:
                    bill_items.append(BillItem(
                        bill=bill,
                        medicine=med,
                        quantity=random.randint(1, 4),
                        price_per_unit=med.price,
                        total_price=med.price * 2 # simplified
                    ))
            
            if bill_items:
                BillItem.objects.bulk_create(bill_items)
