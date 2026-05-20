import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth.models import User

def reset_doctor_passwords():
    # Filter users starting with DOC
    docs = User.objects.filter(username__startswith='DOC')
    count = 0
    for u in docs:
        u.set_password(u.username) # Set password same as username
        u.save()
        count += 1
        print(f"Reset password for {u.username}")
    
    print(f"✅ Reset passwords for {count} doctors.")

if __name__ == "__main__":
    reset_doctor_passwords()
