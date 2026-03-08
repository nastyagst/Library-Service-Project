from rest_framework import serializers
from django.db import transaction

from borrowings.models import Borrowing
from payments.utils import create_stripe_session
from payments.models import Payment


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("id", "borrow_date", "actual_return_date", "user")

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory == 0:
            raise serializers.ValidationError(
                f"Books '{book.title}' is currently out of stock."
            )
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            book.inventory -= 1
            book.save()

            borrowing = super().create(validated_data)

            request = self.context.get("request")
            session = create_stripe_session(borrowing, request)

            Payment.objects.create(
                status="PENDING",
                type="PAYMENT",
                borrowing=borrowing,
                session_url=session.url,
                session_id=session.id,
                money_to_pay=borrowing.book.daily_fee,
            )

            return borrowing
