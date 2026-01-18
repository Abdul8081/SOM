# payments/services.py
import uuid
from decimal import Decimal
from django.db import transaction
from orders.models import Order
from .models import Payment, PaymentStatus


@transaction.atomic
def initiate_payment(*, user, order_id, provider) -> Payment:
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id, user=user)

        if order.status == "PAID":
            raise ValueError("Order already paid")

        payment = Payment.objects.create(
            order=order,
            provider=provider,
            transaction_id=f"txn_{uuid.uuid4().hex}",
            amount=Decimal(order.total_amount),
            status=PaymentStatus.PENDING,
        )

        return payment


@transaction.atomic
def confirm_payment(payment: Payment, success=True):
    if success:
        payment.status = "SUCCESS"
        payment.provider_payment_id = "MOCK123456"
        payment.order.status = "PAID"
    else:
        payment.status = "FAILED"
        payment.order.status = "PAYMENT_FAILED"

    payment.payment.save()
    payment.order.save()

    return payment
