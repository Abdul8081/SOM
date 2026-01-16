from .models import Payment
import uuid


def process_payment(order):
    """
    Mock payment processing.
    This will later be replaced by a real payment gateway.
    """

    payment = Payment.objects.create(
        order=order, status="SUCCESS", transaction_id=str(uuid.uuid4())
    )

    return payment
