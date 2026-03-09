from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token_obtain_pair")
ME_URL = reverse("users:manage")


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
        }

    def test_create_user_success(self):
        res = self.client.post(CREATE_USER_URL, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_token_obtain_success(self):
        get_user_model().objects.create_user(**self.user_data)
        res = self.client.post(TOKEN_URL, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
