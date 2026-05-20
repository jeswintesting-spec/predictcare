import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from hospital.models import Doctor

def setup_roles():
    # 1. Create Groups
    groups = ['Doctor', 'Receptionist', 'Pharmacy']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
    
    password = 'BMH7500'
    
    # 2. Create Receptionist
    recep_user, created = User.objects.get_or_create(username='receptionist', email='reception@bmh.com')
    if created:
        recep_user.set_password(password)
        recep_user.save()
    recep_user.groups.add(Group.objects.get(name='Receptionist'))
    print("Receptionist user ready.")

    # 3. Create Pharmacy
    pharm_user, created = User.objects.get_or_create(username='pharmacy', email='pharmacy@bmh.com')
    if created:
        pharm_user.set_password(password)
        pharm_user.save()
    pharm_user.groups.add(Group.objects.get(name='Pharmacy'))
    print("Pharmacy user ready.")

    # 4. Create Doctor Users
    doctors = Doctor.objects.all()
    group_doc = Group.objects.get(name='Doctor')
    for doc in doctors:
        doc_user, created = User.objects.get_or_create(username=doc.staff_id)
        if created:
            doc_user.email = doc.email or f"{doc.staff_id}@bmh.com"
            doc_user.set_password(password)
            doc_user.save()
        doc_user.groups.add(group_doc)
        # Link doctor name to user first/last name for convenience
        doc_user.first_name = "Dr."
        doc_user.last_name = doc.doctor_name
        doc_user.save()
    print(f"Accounts for {doctors.count()} doctors ready.")

if __name__ == "__main__":
    setup_roles()
