import os
import django
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

import pandas as pd
from ml.predict_load import predict_medicine_demand_from_df
from hospital.models import Visit
from django.db.models.functions import TruncMonth
from django.db.models import Count

# 1. Test prediction
visits_qs = Visit.objects.all().order_by('-visit_date')[:250000].values('department__name', 'visit_date', 'medicines', 'symptoms')
df = pd.DataFrame(list(visits_qs))
df.rename(columns={'department__name': 'department'}, inplace=True)
preds = predict_medicine_demand_from_df(df)
print("Medicine Predictions:")
print(preds)

# 2. Test Monthly Trend aggregation
trend_qs = Visit.objects.annotate(month=TruncMonth('visit_date')).values('month').annotate(c=Count('id')).order_by('month')
monthly_trend = {item['month'].strftime('%Y-%m'): item['c'] for item in trend_qs}
print("\nMonthly Trend:")
print(monthly_trend)

print(f"Total Visits: {sum(monthly_trend.values())}")
