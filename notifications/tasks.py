from celery import shared_task
import time


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_order_created_notification(self, user_id, order_id):
    time.sleep(1)
    print(f"[NOTIFICATION] Order {order_id} created for user {user_id}")


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_payment_success_notification(self, user_id, order_id, amount):
    time.sleep(1)
    print(
        f"[NOTIFICATION] Payment successful for order {order_id} "
        f"(₹{amount}) user {user_id}"
    )
