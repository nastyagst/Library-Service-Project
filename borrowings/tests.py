from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing

BORROWING_URL = reverse("borrowings:borrowing-list")


class BorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com", password="testpass123"
        )
        self.other_user = get_user_model().objects.create_user(
            email="other@user.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)
        self.book = Book.objects.create(
            title="The Hobbit",
            author="J. R. R. Tolkien",
            inventory=12,
            daily_fee=2.0
        )

    def test_user_sees_only_own_borrowings(self):
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date="2026-03-28"
        )
        Borrowing.objects.create(
            user=self.other_user,
            book=self.book,
            expected_return_date="2026-03-28"
        )

        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = res.data["results"] if isinstance(res.data, dict) else res.data

        for item in data:
            self.assertEqual(item["user"], self.user.id)

    def test_create_borrowing_fails_if_inventory_zero(self):
        self.book.inventory = 0
        self.book.save()

        payload = {"book": self.book.id, "expected_return_date": "2026-04-10"}
        res = self.client.post(BORROWING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_borrowing_decreases_inventory(self):
        payload = {"book": self.book.id, "expected_return_date": "2026-04-10"}
        res = self.client.post(BORROWING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 11)
