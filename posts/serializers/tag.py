from rest_framework import serializers

from posts.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'tag',
            'slug',
            'color'
        )
