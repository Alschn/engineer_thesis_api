from django_filters import FilterSet

from posts.models import Comment


class CommentsFilterSet(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'author': ['exact'],
            'post': ['exact'],
            'post__title': ['icontains'],
        }
