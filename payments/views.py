from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from .services import initiate_payment, confirm_payment
from .serializers import PaymentSerializer
from django.shortcuts import get_object_or_404
from .models import Payment


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        order = get_object_or_404(
            Order, id=order_id, user=request.user, status="CREATED"
        )

        payment = initiate_payment(order=order)
        return Response(PaymentSerializer(payment).data)


class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("payment_id")

        payment = get_object_or_404(
            Payment,
            id=payment_id,
            order__user=request.user,
            status="PENDING",
        )

        payment = confirm_payment(payment=payment)
        return Response(PaymentSerializer(payment).data)
