from rest_framework import serializers

from accounts.models import User
from profiles.serializers import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=128,
        write_only=True
    )
    profile = ProfileSerializer(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'profile', 'password'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField()

    # TODO: fields from profile

    class Meta:
        model = User
        fields = (
            'bio',
        )
