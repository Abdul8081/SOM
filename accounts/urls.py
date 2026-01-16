from django.urls import path  # type: ignore[import]
from .views import UserRegisterView, UserProfileView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("me/", UserProfileView.as_view(), name="profile"),
]
