from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PasswordReset
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = ['id', 'email', 'token', 'created_at']
        extra_kwargs = {'token': {'read_only': True}}


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_new_password(self, value):
        
        # Check if the password contains at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")

        # Check if the password contains at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")

        # Check if the password contains at least one digit
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")

        # Check if the password contains at least one special character
        if not re.search(r'[@$!%*?&#]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        # Check if the password is too common or easily guessable
        common_passwords = ["password", "12345678", "qwerty", "letmein", "admin"]
        if value.lower() in common_passwords:
            raise serializers.ValidationError("Password is too common. Please choose a more secure password.")

        return value

