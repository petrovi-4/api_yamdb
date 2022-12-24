import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class SendCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def validate(self, data):
        errors = {}

        if not data.get("username", False):
            errors["username"] = "Это поле обязательно"
        if not data.get("email", False):
            errors["email"] = "Это поле обязательно"
        user = data.get("username", False)
        if user.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        if re.search(r'^[\w.@+-]+\z$', user) is None:
            raise ValidationError(
                (f'Не допустимые символы <{user}> в нике.'),
                params={'value': user},
            )
        if errors:
            raise serializers.ValidationError(errors)

        if User.objects.filter(email=data["email"]):
            user = User.objects.get(email=data["email"])
            if user.username != data["username"]:
                raise serializers.ValidationError(
                    {"email": "Данный username уже зарегистрирован"}
                )
        elif User.objects.filter(username=data["username"]):
            user = User.objects.get(username=data["username"])
            if user.email != data["email"]:
                raise serializers.ValidationError(
                    {"email": "Данный email уже зарегистрирован"}
                )
        return data


class CheckConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[],
    )
    confirmation_code = serializers.CharField()

    def validate(self, data):
        errors = {}
        if not data.get("username", False):
            errors["username"] = "Это поле обязательно"
        else:
            username = data["username"]
            if not User.objects.filter(username=username).exists():
                errors["username"] = "Имя пользователя не найдено"
        if not data.get("confirmation_code", False):
            errors["confirmation_code"] = "Это поле обязательно"

        if errors:
            raise serializers.ValidationError(errors)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "role", "bio")
        read_only_fields = ("role",)
