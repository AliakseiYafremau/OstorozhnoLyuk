from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin, IsModerator
from .custom_schema import *
from .serializers import LoginSerializer, UserSerializer, CreateUserSerializer, UpdateUserSerializer, ChangeAdminSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .simple_jwt_serializers import TokenObtainPairResponseSerializer


# Эндпоинт пользователя
class UserView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdmin()]

    # Возвращаение информации о пользователе
    @swagger_auto_schema(
        operation_description='Получение информации о пользователе. Необходимо быть авторизованным. Никакие параметры не нужны.',
        manual_parameters=[
            header_param,
        ],
        responses={
            200: UserSerializer,
            401: "Некорректные данные"
        },
    )
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    # Создание нового пользователя
    @swagger_auto_schema(
        operation_description='Создание нового пользователя. Необходимо быть администратором.',
        manual_parameters=[
            header_param,
        ],
        request_body=openapi.Schema(
            required=['email', 'password', 'is_moderator', 'is_admin'],
            type=openapi.TYPE_OBJECT,
            properties={
                'email': email_schema,
                'password': password_schema,
                'is_moderator': is_moderator_schema,
                # 'is_admin': is_admin_schema,
            }
        ),
        responses={
            201: UserSerializer,
            400: "Некорректные данные",
            403: "Недостаточно прав"
        }
    )
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            is_moderator = serializer.validated_data.get('is_moderator')
            # is_admin = serializer.validated_data.get('is_admin')
            # user = User.objects.create_user(email=email, password=password,
            #                                 is_moderator=is_moderator, is_admin=is_admin)
            user = User.objects.create_user(email=email, password=password,
                                            is_moderator=is_moderator)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Эндпоинт списка пользователей
class ListUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    # Возвращение списка пользователей
    @swagger_auto_schema(
        operation_description='Получение списка пользователей. Необходимо быть администратором. Никакие параметры не нужны.',
        manual_parameters=[
            header_param,
        ],
        responses={
            200: UserSerializer(many=True),
            401: "Некорректные данные",
            403: "Недостаточно прав"
        },
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# Эндпоинт обновление и удаление пользователя
class UpdateDeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    # Возвращение информации о пользователе
    @swagger_auto_schema(
        operation_description='Получение информации о пользователе. Необходимо быть администратором. Необходим id пользователя в URL.',
        manual_parameters=[
            header_param,
            id_param,
        ],
        responses={
            200: UserSerializer,
            401: "Некорректные данные",
            403: "Недостаточно прав"
        }
    )
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # Обновление информации о пользователе
    @swagger_auto_schema(
        operation_description='Изменение пользователя. Необходимо быть администратором. Необходим id изменяемого пользователя в URL, а также изменяемые данные в теле запроса.',
        manual_parameters=[
            header_param,
            id_param,
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': email_schema,
                'password': password_schema,
                'is_moderator': is_moderator_schema,
                # 'is_admin': is_admin_schema,
            }
        ),
        responses={
            200: UserSerializer,
            401: "Некорректные данные",
            403: "Недостаточно прав"
        }
    )
    def put(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удаление пользователя
    @swagger_auto_schema(
        operation_description='Удаление пользователя. Необходимо быть администратором. '
                              'Необходим id пользователя в URL.',
        manual_parameters=[
            header_param,
            id_param,
        ],
        responses={
            204: "Удалено",
            401: "Некорректные данные",
            403: "Недостаточно прав"
        }
    )
    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Эндпоинт передачи прав администратора
class ChangeAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description='Передача прав администратора.',
        request_body=openapi.Schema(
            required=['id'],
            type=openapi.TYPE_OBJECT,
            properties={
                'id': id_param,
            }
        ),
        responses={
            200: None,
            401: "Некорректные данные",
            403: "Недостаточно прав"
        }
    )
    def post(self, request):
        serializer = ChangeAdminSerializer(data=request.data)
        if serializer.is_valid():
            if not User.objects.filter(id=serializer.validated_data.get('id', None)).exists():
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
            if serializer.validated_data.get('id', None) == request.user.id:
                return Response({'error': 'Вы не можете передать права администратора самому себе'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                current_admin = User.objects.get(id=request.user.id)
                new_admin = User.objects.get(id=serializer.validated_data.get('id', None))
                with transaction.atomic():
                    new_admin.is_admin = True
                    new_admin.is_moderator = True
                    current_admin.is_admin = False
                    current_admin.is_moderator = True
                    new_admin.save()
                    current_admin.save()
                    return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Эндпоинт аутентификации
class LoginView(APIView):

    # Аутентификация. Возвращает JWT-токен
    @swagger_auto_schema(
        operation_description='Аутентификация пользователя.',
        request_body=openapi.Schema(
            required=['email', 'password'],
            type=openapi.TYPE_OBJECT,
            properties={
                'email': email_schema,
                'password': password_schema,
            }
        ),
        responses={
            200: TokenObtainPairResponseSerializer,
            401: "Некорректные данные",
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response({'tokens': data}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description='Обновление JWT-токена',
        request_body=openapi.Schema(
            required=['refresh'],
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': refresh_token_schema,
            }
        ),
        responses={
            200: TokenObtainPairResponseSerializer,
            401: openapi.Response(description="Некорректные данные"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_description='Проверка JWT-токена',
        request_body=openapi.Schema(
            required=['token'],
            type=openapi.TYPE_OBJECT,
            properties={
                'token': token_schema,
            }
        ),
        responses={
            200: openapi.Response(description="Токен валидный"),
            401: openapi.Response(description="Некорректные данные"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description='Аутентификация пользователя. Возвращает JWT-токен',
        request_body=openapi.Schema(
            required=['email', 'password'],
            type=openapi.TYPE_OBJECT,
            properties={
                'email': email_schema,
                'password': password_schema,
            }
        ),
        responses={
            200: TokenObtainPairResponseSerializer,
            401: openapi.Response(description="Некорректные данные"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
