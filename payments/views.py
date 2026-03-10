from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer
from notifications import send_telegram_message


class PaymentViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            return queryset.filter(borrowing__user=self.request.user)
        return queryset

    @action(methods=["GET"], detail=False, url_path="success")
    def success(self, request):
        session_id = request.query_params.get("session_id")

        if not session_id:
            return Response(
                {"error": "No session_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        clean_session_id = session_id.split("?")[0]
        payment = Payment.objects.filter(session_id=clean_session_id).first()

        if payment:
            payment.status = "PAID"
            payment.save()

            user_email = (
                payment.borrowing.user.email
                if payment.borrowing
                else "Unknown User"
            )
            msg = (
                f"<b>Payment Confirmed!</b>\n"
                f"<b>ID: </b> {payment.id}\n"
                f"<b>User: </b> {user_email}\n"
                f"<b>Amount: </b> {payment.money_to_pay}"
            )
            send_telegram_message(msg)

            return Response(
                {"message": "Payment confirmed and status updated!"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "error": "Payment session not found",
                "tried_to_find": clean_session_id
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=["GET"], detail=False, url_path="cancel")
    def cancel(self, request):
        return Response(
            {"message": "Payment cancelled. You can pay later."},
            status=status.HTTP_200_OK,
        )
