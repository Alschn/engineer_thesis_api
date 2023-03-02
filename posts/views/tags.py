from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from core.shared.pagination import page_number_pagination_factory
from posts.filters.tags import TagsFilterSet
from posts.models import Tag
from posts.serializers import TagSerializer

TagsPagination = page_number_pagination_factory(page_size=20, max_page_size=100)


class TagsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    pagination_class = TagsPagination
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filterset_class = TagsFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ('tag',)
