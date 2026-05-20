from django.test import TestCase
from .models import Medicine
from datetime import date

class MedicineTests(TestCase):
    def test_create_medicine(self):
        """Test that we can create a medicine and retrieval works."""
        med = Medicine.objects.create(
            name="TestPill",
            price=10.00,
            stock_quantity=100,
            expiry_date=date(2030, 1, 1)
        )
        self.assertEqual(Medicine.objects.count(), 1)
        self.assertEqual(med.name, "TestPill")
        self.assertEqual(med.stock_quantity, 100)

    def test_stock_update(self):
        """Test stock reduction."""
        med = Medicine.objects.create(
            name="TestPill",
            price=10.00,
            stock_quantity=100,
            expiry_date=date(2030, 1, 1)
        )
        med.stock_quantity -= 10
        med.save()
        med.refresh_from_db()
        self.assertEqual(med.stock_quantity, 90)
