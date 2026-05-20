"""
Django models for PredictCare (Built for BMH Hospital).
Migrated from CSV-based storage to PostgreSQL for production readiness.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Department(models.Model):
    """Hospital department (e.g., Cardiology, Orthopaedics)"""
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    
    class Meta:
        db_table = 'hospital_department'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Doctor(models.Model):
    """Doctor/Physician staff member"""
    staff_id = models.CharField(max_length=20, primary_key=True, unique=True)
    department = models.ForeignKey(
        Department, 
        on_delete=models.PROTECT,  # Prevent deleting department with doctors
        related_name='doctors'
    )
    doctor_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    qualifications = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    work_days = models.CharField(max_length=50)  # e.g., "Mon,Tue,Wed,Thu,Fri"
    shift_type = models.CharField(max_length=20)  # Morning, Afternoon, Evening, Night
    slot_duration = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(120)])  # minutes
    max_patients = models.IntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        db_table = 'hospital_doctor'
        ordering = ['staff_id']
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['doctor_name']),
        ]
    
    def __str__(self):
        return f"{self.staff_id} - {self.doctor_name}"


class Nurse(models.Model):
    """Nurse staff member"""
    staff_id = models.CharField(max_length=20, primary_key=True, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='nurses'
    )
    nurse_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    qualifications = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    work_days = models.CharField(max_length=50)
    shift_type = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'hospital_nurse'
        ordering = ['staff_id']
        indexes = [
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f"{self.staff_id} - {self.nurse_name}"


class Patient(models.Model):
    """Patient record"""
    patient_id = models.CharField(max_length=20, primary_key=True, unique=True)
    patient_name = models.CharField(max_length=200)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    location = models.CharField(max_length=200, blank=True)
    assigned_slot = models.CharField(max_length=50, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hospital_patient'
        ordering = ['patient_id']
        indexes = [
            models.Index(fields=['patient_name']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.patient_id} - {self.patient_name}"


class Visit(models.Model):
    """Patient visit/appointment record"""
    CASE_TYPE_CHOICES = [
        ('Normal', 'Normal'),
        ('Emergency', 'Emergency'),
        ('Critical', 'Critical'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,  # Delete visits when patient is deleted
        related_name='visits'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='visits'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name='visits'
    )
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, default='Normal')
    visit_date = models.DateField()
    medicines = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    slot = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hospital_visit'
        ordering = ['-visit_date', '-created_at']
        indexes = [
            models.Index(fields=['patient', 'visit_date']),
            models.Index(fields=['doctor', 'visit_date']),
            models.Index(fields=['department', 'visit_date']),
            models.Index(fields=['case_type']),
            models.Index(fields=['-visit_date']),
        ]
    
    def __str__(self):
        return f"Visit: {self.patient.patient_id} - {self.visit_date} - {self.department.name}"

class PatientDocument(models.Model):
    """Uploaded documents/reports for a patient"""
    DOCUMENT_TYPES = [
        ('Lab Report', 'Lab Report'),
        ('Prescription', 'Prescription'),
        ('Scan', 'Scan/X-Ray/MRI'),
        ('Discharge Summary', 'Discharge Summary'),
        ('Other', 'Other'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='Other')
    file = models.FileField(upload_to='patient_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'hospital_patientdocument'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['document_type']),
        ]
        
    def __str__(self):
        return f"{self.document_name} ({self.patient.patient_id})"


class HospitalConfiguration(models.Model):
    """Global settings for the hospital (Name, Address, etc. for bills)"""
    hospital_name = models.CharField(max_length=255, default="PREDICTCARE")
    hospital_subtitle = models.CharField(max_length=255, default="Pharmacy & Wellness Center")
    hospital_address = models.TextField(default="123 Healthcare Avenue, Medical District")
    hospital_phone = models.CharField(max_length=50, default="+1 (555) 900-HOSP")
    hospital_email = models.EmailField(default="pharmacy@bmh-hospital.com")
    hospital_footer_text = models.TextField(default="Thank you for choosing PredictCare (BMH Hospital Pharmacy).")
    
    class Meta:
        db_table = 'hospital_configuration'
        verbose_name = "Hospital Configuration"
        verbose_name_plural = "Hospital Configuration"

    def __str__(self):
        return self.hospital_name

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
