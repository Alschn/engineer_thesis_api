from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.db.models import QuerySet
from rest_framework import serializers

from accounts.models import User
from core.shared.serializers import ToRepresentationRequiresUserMixin
from posts.models import Tag, Post
from profiles.models import Profile
from profiles.serializers.profile import EmbeddedProfileSerializer


class TagRelatedField(serializers.RelatedField):
    def get_queryset(self) -> QuerySet[Tag]:
        return Tag.objects.all()

    def to_internal_value(self, data: str) -> Tag:
        lowercase_tag = data.lower()
        tag, created = Tag.objects.get_or_create(tag=lowercase_tag, slug=lowercase_tag)
        return tag

    def to_representation(self, value: Tag):
        return value.tag


class PostSerializer(ToRepresentationRequiresUserMixin, serializers.ModelSerializer):
    author = EmbeddedProfileSerializer(read_only=True)
    is_favourited = serializers.SerializerMethodField()
    tags = TagRelatedField(many=True, read_only=True)

    def __init__(self, *args, user: User | AnonymousUser = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'slug',
            'title',
            'description',
            'body',
            'tags',
            'is_favourited',
            'is_published',
            'favourites_count',
            'created_at',
            'updated_at',
        )

    def get_is_favourited(self, instance: Post) -> bool:
        user = self.user or self.context['request'].user

        if user is None or not user.is_authenticated:
            return False

        return user.profile.added_to_favourites(instance)


class PostListSerializer(ToRepresentationRequiresUserMixin, serializers.ModelSerializer):
    author = EmbeddedProfileSerializer()
    tags = TagRelatedField(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'slug',
            'author',
            'title',
            'description',
            'body',
            'is_published',
            'favourites_count',
            'tags',
            'created_at',
            'updated_at',
        )


class PostCreateSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, allow_empty=False)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'slug',
            'title',
            'description',
            'body',
            'is_published',
            'tags',
            'created_at',
        )
        read_only_fields = ('author', 'slug')

    def __init__(self, *args, author: Profile = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author

    @transaction.atomic
    def create(self, validated_data: dict) -> Post:
        author = self.author or self.context.get('author', None)
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(author=author, **validated_data)
        post.tags.add(*tags)
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, allow_empty=True, required=False)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'slug',
            'title',
            'description',
            'body',
            'tags',
            'is_published',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'slug', 'title', 'created_at', 'updated_at')


class PostFavouriteSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        read_only_fields = PostSerializer.Meta.fields

    def __init__(self, *args, favourite: bool = None, profile: Profile = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.favourite = favourite
        self.profile = profile

    def update(self, instance: Post, validated_data: dict) -> Post:
        favourite = self.favourite
        profile = self.profile or self.context['user'].profile

        if favourite:
            profile.add_to_favourites(instance)
        else:
            profile.remove_from_favourites(instance)

        return instance
