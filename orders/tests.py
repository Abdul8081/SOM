from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from orders.models import Order


class OrderAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="orderuser", password="testpass123"
        )

        # JWT token endpoint
        token_response = self.client.post(
            "/api/v1/token/",
            {
                "username": "orderuser",
                "password": "testpass123",
            },
        )

        self.access_token = token_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.orders_url = "/api/v1/orders/"

    def test_create_order_success(self):
        payload = {
            "items": [
                {"name": "Item A", "quantity": 2, "price": "100.00"},
                {"name": "Item B", "quantity": 1, "price": "50.00"},
            ]
        }

        response = self.client.post(self.orders_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total_amount"], "250.00")

    def test_create_order_without_items_fails(self):
        response = self.client.post(self.orders_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders(self):
        Order.objects.create(user=self.user, total_amount=100)

        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_get_order_detail(self):
        order = Order.objects.create(user=self.user, total_amount=150)

        response = self.client.get(f"/api/v1/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], order.id)

    def test_user_cannot_access_other_users_order(self):
        other_user = User.objects.create_user(
            username="otheruser", password="otherpass"
        )
        order = Order.objects.create(user=other_user, total_amount=300)

        response = self.client.get(f"/api/v1/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
