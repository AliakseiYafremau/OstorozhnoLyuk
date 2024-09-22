from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions

from .models import User
from .permissions import IsAdmin, IsModerator
from .serializers import LoginSerializer, UserSerializer, CreateUserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .simple_jwt_serializers import TokenObtainPairResponseSerializer


class UserView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdmin()]

    @swagger_auto_schema(
        operation_description='Получение информации о пользователе. Необходимо быть авторизованным. Никакие параметры не нужны.',
        responses={
            200: UserSerializer,
            401: "Некорректные данные"
        },
    )
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description='Создание нового пользователя. Необходимо быть администратором.',
        request_body=openapi.Schema(
            required=['email', 'password', 'is_moderator', 'is_admin'],
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Почта пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль пользователя'),
                'is_moderator': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Модератор или нет'),
                'is_admin': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Админ или нет'),
            }
        ),
        responses={
            201: UserSerializer,
            400: "Некорректные данные"
        }
    )
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            is_moderator = serializer.validated_data.get('is_moderator')
            is_admin = serializer.validated_data.get('is_admin')
            user = User.objects.create_user(email=email, password=password,
                                            is_moderator=is_moderator, is_admin=is_admin)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @swagger_auto_schema(
        operation_description='Аутентификация пользователя.',
        request_body=openapi.Schema(
            required=['email', 'password', 'is_moderator', 'is_admin'],
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Почта пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль пользователя'),
            }
        ),
        responses={
            201: TokenObtainPairResponseSerializer,
            401: "Некорректные данные"
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
