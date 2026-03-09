from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from django.contrib.auth import get_user_model

BOOKS_URL = reverse("books:book-list")


class PublicBooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required_for_list(self):
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateBooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com", "password123"
        )
        self.client.force_authenticate(self.user)

    def test_create_book_allowed_for_admin(self):
        payload = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "inventory": 13,
            "daily_fee": "1.50",
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Book.objects.filter(title=payload["title"]).exists()
        self.assertTrue(exists)
