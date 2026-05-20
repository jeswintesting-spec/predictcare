import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

try:
    print(f"Login URL: {reverse('login')}")
    print(f"Home URL: {reverse('home_redirect')}")
    print("URL resolution successful.")
except Exception as e:
    print(f"Error: {e}")
