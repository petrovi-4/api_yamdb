from rest_framework import serializers

from .models import User


class SendCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError('Имя пользователя не может быть "me"')
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "role", "bio")
        read_only_fields = ("role",)
