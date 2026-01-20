from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
import logging

from orders.models import Order
from .services import initiate_payment, confirm_payment
from .serializers import (
    PaymentSerializer,
    InitiatePaymentRequestSerializer,
    ConfirmPaymentRequestSerializer,
)
from .models import Payment

logger = logging.getLogger(__name__)


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=InitiatePaymentRequestSerializer,
        responses=PaymentSerializer,
    )
    def post(self, request):
        try:
            order_id = request.data.get("order_id")
            if not order_id:
                return Response(
                    {"detail": "order_id is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            order = get_object_or_404(
                Order,
                id=order_id,
                user=request.user,
                status="CREATED",
            )

            payment = initiate_payment(order=order)
            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception(
                f"Payment initiation failed for user_id={request.user.id}"
            )
            return Response(
                {"detail": "Unable to initiate payment."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ConfirmPaymentRequestSerializer,
        responses=PaymentSerializer,
    )
    def post(self, request):
        try:
            payment_id = request.data.get("payment_id")
            if not payment_id:
                return Response(
                    {"detail": "payment_id is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment = get_object_or_404(
                Payment,
                id=payment_id,
                order__user=request.user,
                status="PENDING",
            )

            payment = confirm_payment(payment=payment)
            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception(
                f"Payment confirmation failed for user_id={request.user.id}"
            )
            return Response(
                {"detail": "Unable to confirm payment."},
                status=status.HTTP_400_BAD_REQUEST,
            )
