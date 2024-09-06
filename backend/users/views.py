from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import User
from .serializers import LoginSerializer

class UserView(APIView):

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        return Response(user)


# class ListModeratorsView(APIView):

#     def get(self, request):
#         moderators = User.objects.filter(is_moderator=True)
#         return Response(moderators)


class LoginView(APIView):
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
