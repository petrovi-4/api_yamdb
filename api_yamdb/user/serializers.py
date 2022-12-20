import random

from rest_framework import serializers

from .models import User, EmailCodes


class SendCodeSerializer(serializers.ModelSerializer):
    """Сериализация нового пользователя и отправки кода."""

    class Meta:
        model = User
        fields = ["username", "email"]


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового."""

    class Meta:
        model = User
        fields = ["username", "email"]

    # def create(self, validated_data):
    #     print(1)
    #     user = User.objects.get_or_create(
    #         username=validated_data["username"], email=validated_data["email"]
    #     )
    #     return user.token
