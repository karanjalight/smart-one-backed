from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from .utils import get_tokens_for_user
import json

from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from core.models import AuthenticationToken
import uuid




class RegisterUserViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    """
    A simple ViewSet registering users.
    """

    def create(self, request, *args, **kwargs):
        picture = request.data.get('picture', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        return user
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(email=username, password=password)
        
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Expire existing tokens
        AuthenticationToken.objects.filter(user=user).delete()
        
        # Generate a new token
        new_token = AuthenticationToken.objects.create(
            id=uuid.uuid4(),
            access_token=uuid.uuid4().hex,
            expires_in=3600,  # Token valid for 1 hour
            created_at=now(),
            user=user
        )
        
        return Response({
            "token": new_token.access_token,
            "expires_in": new_token.expires_in,
            "user_id": user.id
        }, status=status.HTTP_200_OK)

class ValidateTokenAPIView(APIView):
    def get(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Token required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            auth_token = AuthenticationToken.objects.get(access_token=token)
            if auth_token.is_expired():
                return Response({"error": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"valid": True, "user_id": auth_token.user.id})
        except AuthenticationToken.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
