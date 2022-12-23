import random

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import SendCodeSerializer, UserSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt(request):
    username = request.data.get("username")
    confirmation_code = request.data.get("confirmation_code")
    if not username or not confirmation_code:
        return Response(
            "Одно или несколько обязательных полей пропущены",
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not User.objects.filter(username=username).exists():
        return Response("Имя пользователя неверное", status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)
    if check_password(confirmation_code, user.confirmation_code):
        token = AccessToken.for_user(user)
        return Response({"user": str(token)})

    return Response("Код подтверждения неверен", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_code(request):
    username = request.data.get("username", False)
    email = request.data.get("email", False)
    if not username or not email:
        return Response(
            "Одно или несколько обязательных полей пропущены",
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = SendCodeSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = "".join(map(str, random.sample(range(10), 6)))
        user = User.objects.filter(username=username).exists()
        if not user:
            User.objects.create_user(email=email, username=username)
        User.objects.filter(email=email).update(
            confirmation_code=make_password(
                confirmation_code, salt=None, hasher="default"
            )
        )
        mail_subject = "Код подтверждения для доступа к API! "
        message = f"""
                Здравствуйте!
                Код подтверждения для доступа к API: {confirmation_code}
                С уважением
                Yamdb
                """
        send_mail(
            mail_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        text_message = f"Код отправлен на адрес {email}." " Проверьте раздел SPAM"
        return Response(text_message, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(APIView):
    @permission_classes([permissions.IsAuthenticated])
    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @permission_classes([permissions.IsAuthenticated])
    def patch(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
