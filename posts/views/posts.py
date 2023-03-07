from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
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
from posts.permissions.comments import IsCommentsAuthorPermission
from posts.permissions.post import IsPostAuthorPermission
from posts.serializers import PostSerializer
from posts.serializers.comment import EmbeddedCommentSerializer
from posts.serializers.post import (
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostFavouriteSerializer,
)

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

    GET     /api/posts/favourites/

    POST    /api/posts/

    GET     /api/posts/<str:slug>/

    PATCH   /api/posts/<str:slug>/

    DELETE  /api/posts/<str:slug>/
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthorPermission]
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
        if self.action in ["list", "list_feed", "list_favourites"]:
            return PostListSerializer

        elif self.action == "create":
            return PostCreateSerializer

        elif self.action == "partial_update":
            return PostUpdateSerializer

        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet[Post]:
        if self.action == "list_feed":
            return Post.objects.filter(
                author__in=self.request.user.profile.followed.all()
            ).select_related('author', 'author__user').prefetch_related('tags')

        elif self.action == "list_favourites":
            return self.request.user.profile.favourites.select_related(
                'author', 'author__user').prefetch_related('tags')

        elif self.action in ["comments", "comments_detail"]:
            slug = self.kwargs['slug']
            return Comment.objects.filter(post__slug=slug).select_related('author', 'author__user')

        return Post.objects.select_related('author', 'author__user').prefetch_related('tags')

    def get_serializer(self, *args: Any, **kwargs: Any):
        if self.action == "create":
            return super().get_serializer(*args, **kwargs, author=self.request.user.profile)

        return super().get_serializer(*args, **kwargs)

    @action(
        methods=['GET'], detail=False,
        permission_classes=[IsAuthenticated],
        url_name='feed', url_path='feed',
    )
    def list_feed(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @action(
        methods=['GET'], detail=False,
        permission_classes=[IsAuthenticated],
        url_name='favourites', url_path='favourites'
    )
    def list_favourites(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @action(
        methods=['POST', 'DELETE'], detail=True,
        permission_classes=[IsAuthenticated], serializer_class=PostFavouriteSerializer
    )
    def favourite(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        post = super().get_object()
        serializer = self.get_serializer(
            data={}, instance=post,
            profile=request.user.profile,
            favourite=request.method == 'POST'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @action(
        methods=['GET'], detail=True,
        url_name='comments', url_path='comments',
        lookup_field='id', lookup_url_kwarg='comment_id',
        serializer_class=EmbeddedCommentSerializer,
        pagination_class=CommentsPagination,
        filterset_class=None, filter_backends=[OrderingFilter],
        ordering_fields=('created_at', 'updated_at')
    )
    def comments(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @action(
        methods=['GET', 'DELETE'], detail=True,
        url_name='comments-detail', url_path='comments/(?P<comment_id>[^/.]+)',
        lookup_field='id', lookup_url_kwarg='comment_id',
        serializer_class=EmbeddedCommentSerializer,
        filterset_class=None, filter_backends=[],
        permission_classes=[IsCommentsAuthorPermission]
    )
    def comments_detail(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.method == 'DELETE':
            return super().destroy(request, *args, **kwargs)

        return super().retrieve(request, *args, **kwargs)
