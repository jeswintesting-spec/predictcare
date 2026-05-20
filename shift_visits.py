import os
import django
import random
from datetime import timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Visit

# Shift visits so that the latest visit is today
# Or simply take the last 30 days of visits and compress them into the last 7 days?
# Actually, shifting all visits forward by the difference between today and the max visit date might be the easiest way to preserve patterns!
max_date = Visit.objects.latest('visit_date').visit_date
today = date.today()
delta = today - max_date

if delta.days > 0:
    for v in Visit.objects.all():
        v.visit_date = v.visit_date + delta
        v.save()
    print(f"Shifted visits forward by {delta.days} days")
else:
    print("Visits are already up to today")
