import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from django.contrib.auth import authenticate

def final_check():
    print("--- Final Login Check ---")
    
    # 1. Admin
    admin = authenticate(username="BMH7500", password="BMH7500")
    if admin: print("✅ Admin BMH7500: SUCCESS")
    else: print("❌ Admin BMH7500: FAILED")

    # 2. Doctor 1
    doc1 = authenticate(username="DOC001", password="BMH7500")
    if doc1: print("✅ Doctor DOC001: SUCCESS")
    else: print("❌ Doctor DOC001: FAILED")

    # 3. Doctor 2
    doc2 = authenticate(username="DOC002", password="BMH7500")
    if doc2: print("✅ Doctor DOC002: SUCCESS")
    else: print("❌ Doctor DOC002: FAILED")

if __name__ == "__main__":
    final_check()
