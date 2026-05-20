from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_list, name='pharmacy_inventory'),
    path('billing/', views.billing_view, name='pharmacy_billing'),
    path('billing/manual/', views.manual_billing_view, name='manual_billing'),
    path('billing/history/', views.bill_history, name='bill_history'),
    path('add-medicine/', views.add_medicine, name='add_medicine'),
    path('edit/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
    path('dispense/<int:medicine_id>/', views.dispense_medicine, name='dispense_medicine'),
    path('analytics/', views.pharmacy_analytics, name='pharmacy_analytics'),
    path('bill/<int:bill_id>/print/', views.print_bill, name='print_bill'),
]
