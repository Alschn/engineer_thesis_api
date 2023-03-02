from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.request import Request
from rest_framework.response import Response

from core.shared.pagination import page_number_pagination_factory
from posts.filters.posts import PostsFilterSet
from posts.models import Post, Comment
from posts.serializers import PostSerializer
from posts.serializers.comment import EmbeddedCommentSerializer
from posts.serializers.post import PostListSerializer

PostsPagination = page_number_pagination_factory(
    page_size=25,
    max_page_size=100,
)
CommentsPagination = page_number_pagination_factory(
    page_size=10,
    max_page_size=10,
)


class PostsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    GET     /api/posts/

    GET     /api/posts/feed/

    POST    /api/posts/

    GET     /api/posts/<str:slug>/

    PATCH   /api/posts/<str:slug>/

    DELETE  /api/posts/<str:slug>/
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    filterset_class = PostsFilterSet
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ('title', 'description', 'author__user__username', 'tags__tag')
    ordering_fields = ('id', 'created_at', 'updated_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ["list", "feed"]:
            return PostListSerializer

        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet[Post]:
        if self.action == "feed":
            return Post.objects.filter(
                author__in=self.request.user.profile.followers.all()
            ).select_related('author', 'author__user')

        elif self.action in ["comments", "comments_detail"]:
            slug = self.kwargs['slug']
            return Comment.objects.filter(post__slug=slug).select_related('author', 'author__user')

        return Post.objects.select_related('author', 'author__user')

    @action(
        methods=['GET'], detail=False,
        permission_classes=[IsAuthenticated]
    )
    def feed(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @action(
        methods=['POST', 'DELETE'], detail=True
    )
    def favourite(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        match request.method:
            case 'POST':
                raise NotImplementedError

            case _:
                raise NotImplementedError

    @action(
        methods=['GET'], detail=True,
        serializer_class=EmbeddedCommentSerializer,
        pagination_class=CommentsPagination,
        # todo
        filterset_class=None,
        filter_backends=[],
    )
    def comments(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @action(
        methods=['GET', 'DELETE'], detail=True,
        url_path='comments/(?P<comment_id>\d+)', url_name='comments-detail',
        serializer_class=EmbeddedCommentSerializer,
        lookup_field='id', lookup_url_kwarg='comment_id',
        filterset_class=None,
        filter_backends=[]
    )
    def comments_detail(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        match request.method:
            case 'GET':
                return super().retrieve(request, *args, **kwargs)

            case _:
                return super().destroy(request, *args, **kwargs)
