from urllib import request
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework import status  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
import logging

from .services import create_order, OrderItemRequest
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderCreateRequestSerializer,
)

logger = logging.getLogger(__name__)


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=OrderSerializer(many=True))
    def get(self, request):
        try:
            cache_key = f"user_orders_{request.user.id}"
            cached_orders = cache.get(cache_key)
            if cached_orders:
                return Response(cached_orders, status=status.HTTP_200_OK)

            orders = (
                Order.objects.filter(user=request.user)
                .order_by("-created_at")
            )
            serializer = OrderSerializer(orders, many=True)
            cache.set(cache_key, serializer.data, timeout=300)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception:
            logger.exception(
                f"Failed to fetch orders for user_id={request.user.id}"
            )
            return Response(
                {"detail": "Unable to fetch orders."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        request=OrderCreateRequestSerializer,
        responses=OrderSerializer,
    )
    def post(self, request):
        try:
            items_data = request.data.get("items")
            if not items_data:
                return Response(
                    {"detail": "Order must contain at least one item."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = OrderItemSerializer(data=items_data, many=True)
            serializer.is_valid(raise_exception=True)

            items = [
                OrderItemRequest(**item)
                for item in serializer.validated_data
            ]

            order = create_order(user=request.user, items=items)

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception:
            logger.exception(
                f"Order creation failed for user_id={request.user.id}"
            )
            return Response(
                {"detail": "Order creation failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=OrderSerializer)
    def get(self, request, order_id):
        try:
            order = get_object_or_404(
                Order, id=order_id, user=request.user
            )
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception(
                f"Failed to fetch order_id={order_id} for user_id={request.user.id}"
            )
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class LatestOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cache_key = f"latest_order_{request.user.id}"
            cached_order = cache.get(cache_key)
            if cached_order:
                return Response(cached_order, status=status.HTTP_200_OK)

            order = (
                Order.objects.filter(user=request.user)
                .order_by("-created_at")
                .first()
            )

            if not order:
                return Response(
                    {"detail": "No orders found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = OrderSerializer(order)
            cache.set(cache_key, serializer.data, timeout=300)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception(
                f"Failed to fetch latest order for user_id={request.user.id}"
            )
            return Response(
                {"detail": "Unable to fetch latest order."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
