from rest_framework.routers import DefaultRouter

from .views import (
    PostsViewSet, TagsViewSet, CommentsViewSet
)

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'tags', TagsViewSet, basename='tags')

urlpatterns = router.urls
