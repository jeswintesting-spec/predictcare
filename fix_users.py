import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from hospital.models import Doctor

def fix_users():
    doctors = Doctor.objects.all()
    doctor_group, created = Group.objects.get_or_create(name='Doctor')
    
    created_count = 0
    updated_count = 0
    
    for doc in doctors:
        user, created = User.objects.get_or_create(username=doc.staff_id)
        
        if created:
            print(f"Created User for {doc.staff_id}")
            user.set_password(doc.staff_id)
            user.save()
            created_count += 1
        else:
            # Maybe reset password anyway to be safe?
            # user.set_password(doc.staff_id)
            # user.save()
            pass
            
        # Ensure group
        if not user.groups.filter(name='Doctor').exists():
            user.groups.add(doctor_group)
            print(f"Added {doc.staff_id} to Doctor group")
            updated_count += 1

    print(f"✅ Created {created_count} users.")
    print(f"✅ Updated groups for {updated_count} users.")

if __name__ == "__main__":
    fix_users()
