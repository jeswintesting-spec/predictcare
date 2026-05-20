import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from hospital.models import Doctor

def fix_all_doctor_passwords():
    print("--- 🏥 Setting up Doctor Accounts ---")
    doctors = Doctor.objects.all()
    
    # Ensure Doctor group exists
    doctor_group, _ = Group.objects.get_or_create(name='Doctor')
    
    count = 0
    # Common password for all
    COMMON_PASSWORD = "BMH7500"
    
    for doc in doctors:
        # Create or Get User
        user, created = User.objects.get_or_create(username=doc.staff_id)
        
        # Always reset password to ensure it is BMH7500
        user.set_password(COMMON_PASSWORD)
        user.email = doc.email # sync email too just in case
        user.save()
        
        # Ensure group membership
        if not user.groups.filter(name='Doctor').exists():
            user.groups.add(doctor_group)
            
        count += 1
        
    print(f"✅ Successfully updated {count} doctor accounts.")
    print(f"🔑 All doctor passwords are now set to: '{COMMON_PASSWORD}'")
    print(f"ℹ️  Note: This contains ZEROs (0), not result letter O.")

if __name__ == "__main__":
    fix_all_doctor_passwords()
