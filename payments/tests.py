from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment

PAYMENT_URL = reverse("payments:payment-list")


class PaymentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="password123"
        )
        self.other_user = get_user_model().objects.create_user(
            email="other@test.com", password="password123"
        )
        self.client.force_authenticate(self.user)

        self.book = Book.objects.create(
            title="Test", author="A", inventory=5, daily_fee=2.0
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user, book=self.book, expected_return_date="2026-03-20"
        )
        self.other_borrowing = Borrowing.objects.create(
            user=self.other_user, book=self.book, expected_return_date="2026-03-20"
        )

    def test_user_sees_only_own_payments(self):
        Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.borrowing,
            session_url="http://test.com/1",
            session_id="session_user",
            money_to_pay=20,
        )
        Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.other_borrowing,
            session_url="http://test.com/2",
            session_id="session_other",
            money_to_pay=20,
        )

        res = self.client.get(PAYMENT_URL)
        data = res.data["results"] if isinstance(res.data, dict) else res.data

        session_ids = [item["session_id"] for item in data]
        self.assertIn("session_user", session_ids)
        self.assertNotIn("session_other", session_ids)
        self.assertEqual(len(data), 1)

    def test_admin_sees_all_payments(self):
        self.user.is_staff = True
        self.user.save()

        Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.borrowing,
            session_url="http://test.com/1",
            session_id="session_1",
            money_to_pay=20,
        )
        Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.other_borrowing,
            session_url="http://test.com/2",
            session_id="session_2",
            money_to_pay=20,
        )

        res = self.client.get(PAYMENT_URL)
        data = res.data["results"] if isinstance(res.data, dict) else res.data

        self.assertGreaterEqual(len(data), 2)
