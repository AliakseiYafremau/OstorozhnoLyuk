from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .permissions import IsModerator
from .models import User

class UserView(APIView):

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        return Response(user)


class ListModeratorsView(APIView):

    def get(self, request):
        moderators = User.objects.filter(is_moderator=True)
        return Response(moderators)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)