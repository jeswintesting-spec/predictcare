import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth.models import User

def set_passwords():
    users = User.objects.all()
    count = 0
    for u in users:
        u.set_password('BMH7500') # User requested global password
        u.save()
        count += 1
    
    print(f"✅ Successfully reset passwords for all {count} users to 'BMH7500'.")

if __name__ == "__main__":
    set_passwords()
