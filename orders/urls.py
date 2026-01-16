from django.urls import path  # type: ignore
from .views import OrderListCreateView, OrderDetailView, LatestOrderView

urlpatterns = [
    path("", OrderListCreateView.as_view()),
    path("<int:order_id>/", OrderDetailView.as_view()),
    path("latest/", LatestOrderView.as_view()),
]
