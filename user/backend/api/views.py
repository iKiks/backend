from django.contrib.auth.models import User
from .serializer import UserSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import PasswordReset
from django.urls import reverse
import secrets
from django.utils import timezone
from rest_framework.response import Response
from .tasks import send_reset_email_task
from rest_framework import status

# Create your views here.

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

class UserDelete(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Return queryset filtered by `pk` from URL
        return User.objects.filter(pk=self.kwargs['pk'])

# PasswordReset views
class PasswordResetCreate(generics.CreateAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        token = secrets.token_urlsafe(64)  # Generate a secure token
        instance = serializer.save(token=token)
        email = serializer.validated_data['email']
        reset_link = self.request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'token': token})
        )
        send_reset_email_task(email, reset_link)

class PasswordResetConfirm(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            # Check if the token exists in the PasswordReset model
            password_reset = PasswordReset.objects.get(token=token)
        except PasswordReset.DoesNotExist:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        if (timezone.now() - password_reset.created_at).total_seconds() > 3600:
            return Response({"error": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Reset the password
            user = User.objects.get(email=password_reset.email)
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Optionally delete the PasswordReset instance or mark it as used
            password_reset.delete()

            return Response({"success": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)