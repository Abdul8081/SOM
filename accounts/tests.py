from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AccountAPITests(APITestCase):

    def setUp(self):
        self.register_url = "/api/v1/accounts/register/"
        self.token_url = "/api/v1/token/"

        self.user_data = {"username": "testuser", "password": "testpass123"}

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_user_fails(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success_via_jwt(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(self.token_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.token_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_without_token(self):
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
