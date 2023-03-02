from django_filters import FilterSet

from posts.models import Tag


class TagsFilterSet(FilterSet):
    class Meta:
        model = Tag
        fields = {
            'tag': ['icontains', 'exact'],
            'slug': ['icontains', 'exact'],
        }
