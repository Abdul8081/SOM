from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order, OrderItem
from payments.models import Payment


class PaymentAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="payuser", password="testpass123")

        login = self.client.post(
            "/api/v1/token/",
            {
                "username": "payuser",
                "password": "testpass123",
            },
            format="json",
        )

        self.assertEqual(login.status_code, 200)
        self.token = login.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.order = Order.objects.create(
            user=self.user,
            total_amount=500,
            status="CREATED",
        )

        OrderItem.objects.create(
            order=self.order,
            name="Test Product",
            quantity=1,
            price=500,
        )

    # -------------------------
    # TESTS
    # -------------------------

    def test_create_payment_success(self):
        response = self.client.post(
            "/api/v1/payments/initiate/",
            {"order_id": self.order.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order"], self.order.id)

    def test_create_payment_invalid_order(self):
        response = self.client.post(
            "/api/v1/payments/initiate/",
            {"order_id": 9999},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_duplicate_payment_allowed(self):
        first = self.client.post(
            "/api/v1/payments/initiate/",
            {"order_id": self.order.id},
            format="json",
        )

        second = self.client.post(
            "/api/v1/payments/initiate/",
            {"order_id": self.order.id},
            format="json",
        )

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)

    def test_payment_created_in_db(self):
        self.client.post(
            "/api/v1/payments/initiate/",
            {"order_id": self.order.id},
            format="json",
        )

        payment_exists = Payment.objects.filter(order=self.order).exists()
        self.assertTrue(payment_exists)

    def test_payment_other_user_order_fails(self):
        other_user = User.objects.create_user(
            username="other",
            password="pass123",
        )

        other_order = Order.objects.create(
            user=other_user,
            total_amount=100,
            status="CREATED",
        )

        response = self.client.post(
            "/api/v1/payments/initiate/",
            {"order_id": other_order.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
