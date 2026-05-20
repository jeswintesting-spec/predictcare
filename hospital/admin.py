from django.contrib import admin
from .models import Department, Doctor, Nurse, Patient, Visit

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'doctor_name', 'department', 'specialization', 'phone')
    search_fields = ('doctor_name', 'staff_id', 'specialization')
    list_filter = ('department', 'shift_type')

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'nurse_name', 'department', 'phone')
    search_fields = ('nurse_name', 'staff_id')
    list_filter = ('department', 'shift_type')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'patient_name', 'age', 'gender', 'location', 'doctor')
    search_fields = ('patient_name', 'patient_id')
    list_filter = ('gender', 'location')
    date_hierarchy = 'created_at'

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('visit_date', 'patient', 'doctor', 'department', 'case_type')
    search_fields = ('patient__patient_name', 'doctor__doctor_name')
    list_filter = ('case_type', 'department', 'visit_date')
    date_hierarchy = 'visit_date'
