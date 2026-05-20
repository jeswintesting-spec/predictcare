import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import Doctor, Department

qs = Doctor.objects.values('department__name').annotate(count=django.db.models.Count('staff_id'))
for q in qs:
    print(q['department__name'], q['count'])

