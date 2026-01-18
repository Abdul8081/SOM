# payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .services import initiate_payment, confirm_payment
from .serializers import PaymentSerializer


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        provider = request.data.get("provider", "mock")

        payment = initiate_payment(
            user=request.user,
            order_id=order_id,
            provider=provider,
        )

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("payment_id")
        success = request.data.get("success", True)

        payment = Payment.objects.get(id=payment_id)
        payment = confirm_payment(payment, success)

        return Response(PaymentSerializer(payment).data)
