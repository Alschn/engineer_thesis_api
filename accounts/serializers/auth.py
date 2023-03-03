import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as BaseTokenRefreshSerializer,
    TokenVerifySerializer as BaseTokenVerifySerializer,
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer
)

from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    username = serializers.CharField(
        min_length=6, max_length=30
    )
    email = serializers.EmailField()
    password1 = serializers.CharField(
        label='Password',
        write_only=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        label='Confirm Password',
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password1',
            'password2',
        )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email is already taken.", code='unique'
            )
        return value

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username is already taken.", code='unique'
            )
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields do not match."}
            )

        password1 = attrs['password1']

        try:
            validators.validate_password(password=password1)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"password": list(e.messages)}
            )

        return attrs

    def create(self, validated_data: dict) -> User:
        password1 = validated_data.pop('password1')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class TokenRefreshSerializer(BaseTokenRefreshSerializer):

    def validate(self, attrs: dict) -> dict:
        return super().validate(attrs)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class TokenVerifySerializer(BaseTokenVerifySerializer):

    def validate(self, attrs: dict) -> dict:
        return super().validate(attrs)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
