from urllib import request
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import AllowAny, IsAuthenticated  # type: ignore
from rest_framework import status  # type: ignore
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

from .serializers import UserRegisterSerializer, UserProfileSerializer


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        responses=UserProfileSerializer,
    )
    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            logger.info(
                f"User registered successfully: id={user.id}, username={user.username}"
            )

            return Response(
                UserProfileSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.exception("Error occurred during user registration")
            return Response(
                {"detail": "User registration failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            logger.info(f"Profile fetch requested for user_id={request.user.id}")

            cache_key = f"user_profile_{request.user.id}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)

            serializer = UserProfileSerializer(request.user)
            cache.set(cache_key, serializer.data, timeout=300)  # 5 minutes

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(
                f"Error occurred while fetching profile for user_id={request.user.id}"
            )
            return Response(
                {"detail": "Unable to fetch user profile."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# TODO: user deletion from django-admin have to implement
