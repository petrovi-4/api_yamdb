from rest_framework import serializers

from access.models import User


class SendCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "role", "bio")
        read_only_fields = ("role",)
