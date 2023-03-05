from rest_framework import serializers

from posts.models import Comment, Post
from profiles.models import Profile
from profiles.serializers.profile import EmbeddedProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = EmbeddedProfileSerializer()

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

    def __init__(self, *args, post: Post = None, author: Profile = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.post = post
        self.author = author

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
        read_only_fields = ('post', 'author', 'created_at', 'updated_at')

    def create(self, validated_data: dict) -> Comment:
        post = self.post or self.context['post']
        author = self.author or self.context['author']

        return Comment.objects.create(
            author=author,
            post=post,
            **validated_data
        )


class EmbeddedCommentSerializer(serializers.ModelSerializer):
    author = EmbeddedProfileSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'created_at',
            'updated_at',
        )
