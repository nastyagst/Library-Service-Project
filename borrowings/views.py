from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer
from notifications import send_telegram_message


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        user = self.request.user

        if not user.is_staff:
            return queryset.filter(user=user)

        return queryset


    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        message = (
            f"<b>New Borrowing!</b>\n"
            f"User: {borrowing.user.email}\n"
            f"Book: {borrowing.book.title}\n"
            f"Return date: {borrowing.expected_return_date}"
        )

        send_telegram_message(message)

    @action(methods=["POST"], detail=True, url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"error": "This book has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = timezone.now().date()
        book = borrowing.book
        book.inventory += 1
        book.save()
        borrowing.save()

        return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_200_OK)
