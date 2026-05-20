
import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from pharmacy.models import PharmacyBill
from django.utils import timezone

def smear_dates():
    print("Smearing pharmacy bill dates to create a trend...")
    bills = list(PharmacyBill.objects.all())
    count = len(bills)
    print(f"Processing {count} bills...")
    
    # We want a trend over the last 60 days
    now = timezone.now()
    
    # Update in chunks for efficiency
    updated_count = 0
    for i, bill in enumerate(bills):
        # Random date between 60 days ago and now
        random_days = random.random() * 60
        new_date = now - timedelta(days=random_days)
        bill.created_at = new_date
        
        if (i + 1) % 5000 == 0:
            PharmacyBill.objects.bulk_update(bills[i-4999:i+1], ['created_at'])
            updated_count += 5000
            print(f"Progress: {updated_count}/{count} bills updated...")

    # Final chunk
    remaining = count % 5000
    if remaining:
        PharmacyBill.objects.bulk_update(bills[count-remaining:count], ['created_at'])
        updated_count += remaining
        
    print(f"✅ Successfully smeared {updated_count} bills across the last 60 days.")

if __name__ == "__main__":
    smear_dates()
