# payments/serializers.py
from rest_framework import serializers  # type: ignore
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("status", "provider_payment_id")
