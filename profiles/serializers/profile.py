from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from accounts.models import User
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    is_following_you = serializers.SerializerMethodField()
    is_followed_by_you = serializers.SerializerMethodField()

    def __init__(self, *args, user: User | AnonymousUser = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'email',
            'bio',
            'image',
            'is_following_you',
            'is_followed_by_you',
        )

    def get_is_following_you(self, instance: Profile) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        follower = instance
        followee = user.profile
        return follower.is_following(followee)

    def get_is_followed_by_you(self, instance: Profile) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        follower = user.profile
        followee = instance
        return followee.is_followed_by(follower)


class ProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    is_following_you = serializers.SerializerMethodField()
    is_followed_by_you = serializers.SerializerMethodField()

    def __init__(self, *args, user: User | AnonymousUser = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'image',
            'is_following_you',
            'is_followed_by_you',
        )

    def get_is_following_you(self, instance: Profile) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        follower = instance
        followee = user.profile
        return follower.is_following(followee)

    def get_is_followed_by_you(self, instance: Profile) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        follower = user.profile
        followee = instance
        return followee.is_followed_by(follower)


class EmbeddedProfileSerializer(ProfileSerializer):
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'email',
            'image',
            'is_followed_by_you',
        )
