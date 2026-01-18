from celery import shared_task
from django.contrib.auth import get_user_model

from .email import send_email
from .sms import send_sms
from .services import (
    order_created_message,
    payment_success_message,
)

User = get_user_model()


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_order_created_notification(self, user_id, order_id):
    user = User.objects.get(id=user_id)

    subject, message = order_created_message(order_id)

    if user.email:
        send_email(subject, message, user.email)

    # mock phone
    send_sms("9999999999", message)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_payment_success_notification(self, user_id, order_id, amount):
    user = User.objects.get(id=user_id)

    subject, message = payment_success_message(order_id, amount)

    if user.email:
        send_email(subject, message, user.email)

    send_sms("9999999999", message)
