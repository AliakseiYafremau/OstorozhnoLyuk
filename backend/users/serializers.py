from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    is_moderator = serializers.BooleanField()
    is_admin = serializers.BooleanField()


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    is_moderator = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    