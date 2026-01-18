from django.urls import path
from .views import InitiatePaymentView, ConfirmPaymentView

urlpatterns = [
    path("", InitiatePaymentView.as_view()),  # 👈 default
    path("initiate/", InitiatePaymentView.as_view()),
    path("confirm/", ConfirmPaymentView.as_view()),
]
