from django.db import models  # type: ignore
from orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)  # stripe
    provider_payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"


# payments/models.py


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
