from django_filters import FilterSet

from posts.models import Post


class PostsFilterSet(FilterSet):
    class Meta:
        model = Post
        fields = {
            'slug': ['icontains', 'exact'],
            'title': ['icontains'],
            'description': ['icontains'],
            'author__user__username': ['icontains'],
            'author__user__email': ['icontains'],
            'tags__tag': ['icontains'],
            'created_at': ['gte', 'lte'],
        }
