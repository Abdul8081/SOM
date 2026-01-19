from celery import shared_task
from django.contrib.auth import get_user_model

from notifications.email import send_email
from notifications.services import (
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
        
    # TODO Implement logging for failed email attempts
    # else:
    #     throw ValueError("User does not have an email address.")

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_payment_success_notification(self, user_id, order_id, amount):
    user = User.objects.get(id=user_id)

    subject, message = payment_success_message(order_id, amount)

    if user.email:
        send_email(subject, message, user.email)
    # else:
    #     throw ValueError("User does not have an email address.")
