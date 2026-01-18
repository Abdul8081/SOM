from django.test import TestCase
from unittest.mock import patch

from notifications.tasks import (
    send_order_created_notification,
    send_payment_success_notification,
)


class NotificationTaskTests(TestCase):

    @patch("notifications.tasks.time.sleep")
    @patch("builtins.print")
    def test_order_created_notification_prints_message(self, mock_print, mock_sleep):
        send_order_created_notification(
            user_id=1,
            order_id=101,
        )

        mock_sleep.assert_called_once_with(1)
        mock_print.assert_called_once_with(
            "[NOTIFICATION] Order 101 created for user 1"
        )

    @patch("notifications.tasks.time.sleep")
    @patch("builtins.print")
    def test_payment_success_notification_prints_message(self, mock_print, mock_sleep):
        send_payment_success_notification(
            user_id=2,
            order_id=202,
            amount=499,
        )

        mock_sleep.assert_called_once_with(1)
        mock_print.assert_called_once_with(
            "[NOTIFICATION] Payment successful for order 202 (₹499) user 2"
        )

    # -------------------------------
    # NEW TEST CASES
    # -------------------------------

    @patch("notifications.tasks.time.sleep", side_effect=Exception("fail"))
    def test_order_created_notification_retries_on_exception(self, mock_sleep):
        with self.assertRaises(Exception):
            send_order_created_notification(
                user_id=1,
                order_id=101,
            )

        mock_sleep.assert_called_once()

    @patch("notifications.tasks.time.sleep", side_effect=Exception("fail"))
    def test_payment_success_notification_retries_on_exception(self, mock_sleep):
        with self.assertRaises(Exception):
            send_payment_success_notification(
                user_id=2,
                order_id=202,
                amount=499,
            )

        mock_sleep.assert_called_once()

    @patch("notifications.tasks.time.sleep")
    @patch("builtins.print")
    def test_notification_tasks_return_none(self, mock_print, mock_sleep):
        result1 = send_order_created_notification(
            user_id=1,
            order_id=101,
        )
        result2 = send_payment_success_notification(
            user_id=2,
            order_id=202,
            amount=499,
        )

        self.assertIsNone(result1)
        self.assertIsNone(result2)
