from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer


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
            return Response({"error": "No session_id"}, status=400)

        clean_session_id = session_id.split("?")[0]

        payment = Payment.objects.filter(session_id=clean_session_id).first()

        if payment:
            payment.status = "PAID"
            payment.save()
            return Response({"message": "Payment confirmed!"}, status=200)

        return Response(
            {"error": "Not found", "tried_to_find": clean_session_id}, status=400
        )

    @action(methods=["GET"], detail=False, url_path="cancel")
    def cancel(self, request):
        return Response(
            {"message": "Payment cancelled. You can pay later."},
            status=status.HTTP_200_OK,
        )
