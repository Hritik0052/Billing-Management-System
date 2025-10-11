from django.db import models
from accounts.models import User
from items.models import Item

class Bill(models.Model):
    bill_no = models.IntegerField(unique=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    customer_phone = models.CharField(max_length=15, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill {self.bill_no} - {self.customer_name}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
