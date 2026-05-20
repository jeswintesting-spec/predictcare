from django.db import models
from django.core.validators import MinValueValidator
from hospital.models import Visit

CATEGORY_CHOICES = [
    ('Tablet', 'Tablet'),
    ('Capsule', 'Capsule'),
    ('Syrup', 'Syrup'),
    ('Injection', 'Injection'),
    ('Ointment/Cream', 'Ointment/Cream'),
    ('Drops', 'Drops'),
    ('Inhaler', 'Inhaler'),
    ('General/Consumable', 'General/Consumable'),
]

class Medicine(models.Model):
    """Represents a medicine in the inventory."""
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General/Consumable')
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    rack_location = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    min_stock_level = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Stock: {self.stock_quantity})"

class PrescriptionLine(models.Model):
    """
    Represents a specific medicine prescribed during a visit.
    This replaces the text-based 'medicines' field in Visit.
    """
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='prescribed_in')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    dosage_instructions = models.CharField(max_length=200, help_text="e.g. 1-0-1 after food")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"

class PharmacyBill(models.Model):
    """Represents a final bill/invoice generated."""
    customer_name = models.CharField(max_length=200, help_text="Patient name or Walk-in Customer")
    patient = models.ForeignKey('hospital.Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='pharmacy_bills')
    
    # Financial Breakdown
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Bill #{self.id} - {self.customer_name}"

class BillItem(models.Model):
    """Line item in a pharmacy bill."""
    bill = models.ForeignKey(PharmacyBill, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"
