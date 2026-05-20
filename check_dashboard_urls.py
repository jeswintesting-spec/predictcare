import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

try:
    print(f"Hub URL: {reverse('hub')}")
    print(f"Admin Dashboard: {reverse('admin_dashboard')}")
    print(f"Reception Dashboard: {reverse('reception_dashboard')}")
    print(f"Doctor Dashboard: {reverse('doctor_dashboard')}")
    print("Dashboard URLs resolution successful.")
except Exception as e:
    print(f"Error: {e}")
