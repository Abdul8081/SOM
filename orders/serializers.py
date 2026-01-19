# from rest_framework import serializers  # type: ignore
# from .models import Order, OrderItem
# from decimal import Decimal


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ["name", "quantity", "price"]

#     def validate_quantity(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Quantity must be greater than zero.")
#         return value

#     def validate_price(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Price must be greater than zero.")
#         return value


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = ["id", "items", "total_amount", "status", "created_at"]
#         read_only_fields = ["total_amount", "status", "created_at"]


from rest_framework import serializers
from .models import Order, OrderItem
from decimal import Decimal


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["name", "quantity", "price"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "items", "total_amount", "status", "created_at"]
        read_only_fields = ["total_amount", "status", "created_at"]


# Swagger-only request serializer (DOES NOT affect logic)
class OrderCreateRequestSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)
