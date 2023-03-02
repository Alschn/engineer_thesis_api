from rest_framework.routers import DefaultRouter

from .views import ProfilesViewSet

router = DefaultRouter()
router.register(r'profiles', ProfilesViewSet, basename='profiles')

urlpatterns = router.urls
