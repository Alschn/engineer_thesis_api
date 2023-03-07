from rest_framework import serializers

from core.shared.serializers import ToRepresentationRequiresUserMixin
from posts.models import Comment, Post
from profiles.serializers.profile import EmbeddedProfileSerializer


class CommentSerializer(ToRepresentationRequiresUserMixin, serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    author = EmbeddedProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'post',
            'body',
            'created_at',
            'updated_at',
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())
    body = serializers.CharField(max_length=1000, allow_blank=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'post',
            'author',
            'body',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('author', 'created_at', 'updated_at')


class EmbeddedCommentSerializer(ToRepresentationRequiresUserMixin, serializers.ModelSerializer):
    author = EmbeddedProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'created_at',
            'updated_at',
        )
