from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework import status  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from .services import create_order, OrderRequest, OrderItemRequest

# from .serializers import OrderCreateSerializer
from .services import create_order

from .models import Order
from .serializers import (
    OrderItemSerializer,
    OrderSerializer,
)


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        items_data = request.data.get("items")
        if not items_data:
            return Response(
                {"detail": "Order must contain at least one item."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderItemSerializer(data=items_data, many=True)
        serializer.is_valid(raise_exception=True)

        items = [OrderItemRequest(**item) for item in serializer.validated_data]

        order = create_order(user=request.user, items=items)

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return Response(OrderSerializer(order).data)

    ## if delete functionality is needed in future ##
    # def delete(self, request, order_id):
    #     order = get_object_or_404(Order, id=order_id, user=request.user)

    #     if order.status == "PAID":
    #         return Response(
    #             {"error": "Paid orders cannot be deleted."},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     order.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class LatestOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.filter(user=request.user).order_by("-created_at").first()

        if not order:
            return Response(
                {"detail": "No orders found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(OrderSerializer(order).data)
