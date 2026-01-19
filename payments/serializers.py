from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "transaction_id",
            "provider_payment_id",
            "status",
            "created_at",
        )
        
# 🔹 Swagger-only serializers (DO NOT affect logic)

class InitiatePaymentRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()


class ConfirmPaymentRequestSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()

