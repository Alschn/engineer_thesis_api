from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from core.shared.pagination import page_number_pagination_factory
from posts.filters.comments import CommentsFilterSet
from posts.models import Comment
from posts.serializers import CommentSerializer
from posts.serializers.comment import CommentCreateSerializer

CommentsPagination = page_number_pagination_factory(
    page_size=25, max_page_size=50
)


class CommentsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    filterset_class = CommentsFilterSet
    pagination_class = CommentsPagination
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ('body', 'author__username', 'post__title')
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer

        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet[Comment]:
        return Comment.objects.select_related('author', 'author__user').all()

    def perform_create(self, serializer: CommentCreateSerializer) -> None:
        serializer.save(author=self.request.user.profile)
