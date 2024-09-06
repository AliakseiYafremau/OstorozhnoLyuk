from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.Serializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_moderator', 'is_admin']
