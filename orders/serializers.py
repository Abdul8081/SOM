from rest_framework import serializers  # type: ignore
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "items", "total_amount", "status", "created_at"]
        read_only_fields = ["total_amount", "status", "created_at"]
