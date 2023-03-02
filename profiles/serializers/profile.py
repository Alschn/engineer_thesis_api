from rest_framework import serializers

from accounts.models import User
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    is_following_you = serializers.SerializerMethodField()
    is_followed_by_you = serializers.SerializerMethodField()

    def __init__(self, *args, user: User = None, **kwargs):
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

        followee = user.profile
        follower = instance
        return followee.is_followed_by(follower)

    def get_is_followed(self, instance: Profile) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        follower = user.profile
        followee = instance
        return follower.is_following(followee)


class ProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    is_following_you = serializers.SerializerMethodField()
    is_followed_by_you = serializers.SerializerMethodField()

    def __init__(self, *args, user: User = None, **kwargs):
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

        followee = user.profile
        follower = instance
        return followee.is_followed_by(follower)

    def get_is_followed_by_you(self, instance: Profile) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        follower = user.profile
        followee = instance
        return follower.is_following(followee)


class EmbeddedProfileSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'image',
        )
