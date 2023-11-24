from rest_framework.authtoken.models import Token
from django.shortcuts import render
from requests import Response
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from users.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from certificates.models import Certificate
from certificates.serializers import CertificateSerializer

# Get all Users
class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#POST method
class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Get, PUT, DELETE methods
class UserApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginApiView(APIView):
    @permission_classes([AllowAny])
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate username and password
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            login(request, user)

            # Retrieve certificates based on user's superuser status
            if user.is_superuser:
                certificates = Certificate.objects.all()
            else:
                certificates = Certificate.objects.filter(user=user)

            # Serialize the certificates
            certificate_serializer = CertificateSerializer(certificates, many=True)

            response_data = {
                'success': True,
                'user_id': user.id,
                'is_superuser': user.is_superuser,
                'certificates': certificate_serializer.data,
            }

            # Debug print statement
            print(f"Response data: {response_data}")

            return JsonResponse(response_data)
        else:
            # User does not exist or invalid credentials
            existing_user = User.objects.filter(username=username).first()
            if existing_user:
                # User exists in the database
                return JsonResponse({'error': 'Invalid credentials. User exists, but the password is incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # User does not exist in the database
                return JsonResponse({'error': 'User does not exist in the database.'}, status=status.HTTP_404_NOT_FOUND)
            

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        # Customize the response data to include the user ID
        response_data = {
            'token': Token.objects.get(user=user).key,
            'user_id': user.id,
        }

        return Response(response_data)