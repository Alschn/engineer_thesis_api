from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from core.shared.pagination import page_number_pagination_factory
from posts.filters.comments import CommentsFilterSet
from posts.models import Comment
from posts.serializers import CommentSerializer

CommentsPagination = page_number_pagination_factory(
    page_size=10, max_page_size=50
)


class CommentsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    filterset_class = CommentsFilterSet
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ('body', 'author__username', 'post__title')
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    def get_queryset(self) -> QuerySet[Comment]:
        return Comment.objects.select_related('author', 'author__user').all()
