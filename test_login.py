import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def test_login(username, password):
    user = authenticate(username=username, password=password)
    if user:
        print(f"✅ Login SUCCESS for {username}")
        return True
    else:
        print(f"❌ Login FAILED for {username}")
        # Check if user exists
        if User.objects.filter(username=username).exists():
            print(f"   (User {username} exists, maybe password wrong?)")
        else:
            print(f"   (User {username} DOES NOT EXIST)")
        return False

print("--- Testing Login ---")
# Try Admin
test_login('BMH7500', 'BMH7500') # Assuming password is same as username for legacy
# Try Doctor
test_login('DOC001', 'DOC001') # Assuming password is strictly legacy ID
test_login('DOC001', 'password') # Try common default
