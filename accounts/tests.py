from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountAPITests(APITestCase):

    def setUp(self):
        # Use actual API paths (NO reverse)
        self.register_url = "/api/v1/accounts/register/"
        self.token_url = "/api/v1/token/"
        self.profile_url = "/api/v1/accounts/me/"

        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongPass123",
        }

    # 1️⃣ Register user successfully
    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])

    # 2️⃣ Register fails without email
    def test_register_user_without_email_fails(self):
        data = {
            "username": "nouseremail",
            "password": "StrongPass123",
        }

        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    # 3️⃣ Register fails with weak password
    def test_register_user_with_short_password_fails(self):
        data = {
            "username": "weakuser",
            "email": "weak@example.com",
            "password": "123",
        }

        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    # 4️⃣ Login success
    def test_login_success(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.token_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # 5️⃣ Login fails with wrong password
    def test_login_invalid_credentials(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.token_url,
            {
                "username": self.user_data["username"],
                "password": "WrongPassword",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 6️⃣ Authenticated user can access profile
    def test_get_user_profile_authenticated(self):
        User.objects.create_user(**self.user_data)

        login = self.client.post(
            self.token_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )

        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])
