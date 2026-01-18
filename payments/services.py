from django.db import transaction
from .models import Payment
from .providers.mock import MockPaymentProvider


@transaction.atomic
def initiate_payment(*, order):
    if hasattr(order, "payment"):
        return order.payment  # idempotent

    provider = MockPaymentProvider()

    response = provider.initiate(order.total_amount)

    payment = Payment.objects.create(
        order=order,
        provider="mock",
        amount=order.total_amount,
        transaction_id=response["transaction_id"],
        provider_payment_id=response["provider_payment_id"],
        status="PENDING",
    )

    return payment


@transaction.atomic
def confirm_payment(*, payment):
    provider = MockPaymentProvider()
    response = provider.confirm(payment.provider_payment_id)

    if response["status"] == "SUCCESS":
        payment.status = "SUCCESS"
        payment.save(update_fields=["status"])

        # update order
        order = payment.order
        order.status = "PAID"
        order.save(update_fields=["status"])

    return payment
