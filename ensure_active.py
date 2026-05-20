import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth.models import User

def activate_all_users():
    users = User.objects.all()
    count = 0
    for u in users:
        if not u.is_active:
            u.is_active = True
            u.save()
            count += 1
            print(f"Activated user: {u.username}")
    
    # Re-verify BMH7500
    u = User.objects.get(username='BMH7500')
    if not u.check_password('BMH7500'):
        print("Resetting BMH7500 password just to be sure")
        u.set_password('BMH7500')
        u.save()

    print(f"✅ Ensured all users active. Activated {count} inactive users.")

if __name__ == "__main__":
    activate_all_users()
