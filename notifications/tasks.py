from celery import shared_task  # type: ignore
import time


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_notification(self, user_id, message):
    time.sleep(1)  # mock delay
    print(f"Notification to {user_id}: {message}")
