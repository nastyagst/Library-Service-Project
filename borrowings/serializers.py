from rest_framework import serializers
from django.db import transaction

from borrowings.models import Borrowing


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
            return super().create(validated_data)
