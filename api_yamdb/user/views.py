import random

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import (
    UserSerializer,
    CheckConfirmationCodeSerializer,
    SendCodeSerializer,
    IsNotAdminUserSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_code(request):
    """Отправка кода для авторизации"""
    serializer = SendCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data.get("email", False)
        username = request.data.get("username", False)
        confirmation_code = "".join(map(str, random.sample(range(10), 6)))
        if not User.objects.filter(username=username, email=email).exists():
            user = User.objects.create(username=username, email=email)
        else:
            user = User.objects.get(username=username, email=email)
        user.confirmation_code = make_password(
            confirmation_code, salt=None, hasher="default"
        )
        user.save()

        send_mail(
            "Code",
            confirmation_code,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return Response(serializer.initial_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt(request):
    """Получение JWT токена"""
    username = request.data.get("username")
    confirmation_code = request.data.get("confirmation_code")
    serializer = CheckConfirmationCodeSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            user.confirmation_code = 0
            user.save()
            return Response({"token": str(token)})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == "PATCH":
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user, data=request.data, partial=True
                )
            else:
                serializer = IsNotAdminUserSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Вы не авторизованы", status=status.HTTP_401_UNAUTHORIZED)
