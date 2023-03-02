from django.db import transaction
from rest_framework import serializers

from accounts.models import User
from posts.models import Tag, Post
from profiles.models import Profile
from profiles.serializers.profile import EmbeddedProfileSerializer


class TagRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data: str) -> Tag:
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())
        return tag

    def to_representation(self, value: Tag):
        return value.tag


class PostSerializer(serializers.ModelSerializer):
    author = EmbeddedProfileSerializer()
    favourited = serializers.SerializerMethodField()
    tag_list = TagRelatedField(many=True, source='tags')

    def __init__(self, *args, user: User = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Post
        fields = (
            'author',
            'body',
            'description',
            'favourited',
            'favourites_count',
            'slug',
            'tag_list',
            'title',
            'created_at',
            'updated_at',
        )

    def get_favourited(self, instance: Post) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        return user.profile.added_to_favourites(instance)


class PostListSerializer(serializers.ModelSerializer):
    author = EmbeddedProfileSerializer()
    tag_list = TagRelatedField(many=True, source='tags')

    class Meta:
        model = Post
        fields = (
            'id',
            'slug',
            'author',
            'title',
            'description',
            'body',
            'favourites_count',
            'tag_list',
            'created_at',
            'updated_at',
        )


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'body',
            'description',
            'slug',
            'title',
        )

    def __init__(self, *args, user: User = None, author: Profile = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.author = author

    @transaction.atomic
    def create(self, validated_data: dict) -> Post:
        author = self.author or self.context.get('author', None)
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(author=author, **validated_data)
        post.tags.add(*tags)
        return post
