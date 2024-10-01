from rest_framework import serializers

from users.models import User


# Сериализатор для аутентификации
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


# Сериализатор для пользователя
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    is_moderator = serializers.BooleanField()
    is_admin = serializers.BooleanField()


# Сериализатор для создания пользователя
class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    is_moderator = serializers.BooleanField()
    # is_admin = serializers.BooleanField()


class UpdateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    is_moderator = serializers.BooleanField(required=False)
    # is_admin = serializers.BooleanField(required=False)

    def update(self, instance, data):
        instance.email = data.get('email', instance.email)
        instance.is_moderator = data.get('is_moderator', instance.is_moderator)
        # instance.is_admin = data.get('is_admin', instance.is_admin)

        instance.save()
        return instance


# Сериализатор для замены администратор.
# Сделана, так как на сайте не может быть более одного администратора.
class ChangeAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
