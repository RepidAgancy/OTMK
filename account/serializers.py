from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from account import models


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data['phone_number']
        password = data['password']

        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})

        if not user.is_active:
            raise serializers.ValidationError({'detail': 'User account is disabled'})

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        token = RefreshToken.for_user(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
            'role': user.role if user.role else None,
        }


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'phone_number', 'profile_image']
