import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from hospital.models import Doctor

def verify_doctor_status():
    print("--- Verifying Doctor Login Status ---")
    
    # 1. Check if DOC001 exists as a Doctor
    try:
        doc = Doctor.objects.get(staff_id="DOC001")
        print(f"✅ Doctor object found: {doc.staff_id} - {doc.doctor_name}")
    except Doctor.DoesNotExist:
        print(f"❌ Doctor DOC001 NOT found in Doctor table!")
        return

    # 2. Check if User exists for DOC001
    try:
        user = User.objects.get(username="DOC001")
        print(f"✅ User object found: {user.username}")
    except User.DoesNotExist:
        print(f"❌ User DOC001 NOT found in auth_user table! (This is the issue)")
        # Attempt to create it if missing, just for testing
        return

    # 3. Test Authentication with BMH7500
    user_auth = authenticate(username="DOC001", password="BMH7500")
    if user_auth:
        print(f"✅ Authentication SUCCESS with password 'BMH7500'")
    else:
        print(f"❌ Authentication FAILED with password 'BMH7500'")
        print("   Resetting password explicitly to 'BMH7500' now...")
        user.set_password("BMH7500")
        user.save()
        print("   Password reset. Testing again...")
        if authenticate(username="DOC001", password="BMH7500"):
             print("   ✅ Re-test SUCCESS.")
        else:
             print("   ❌ Re-test FAILED. Something is very wrong.")

if __name__ == "__main__":
    verify_doctor_status()
