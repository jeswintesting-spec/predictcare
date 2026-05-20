import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Doctor

print("Total Doctors:", Doctor.objects.count())
shifts = Doctor.objects.values('shift_type').annotate(c=django.db.models.Count('staff_id'))
print("Shifts:", list(shifts))
