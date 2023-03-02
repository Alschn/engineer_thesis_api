from django.contrib import admin
from django.urls import path, include

from core.schema.views import (
    SchemaAPIView,
    SchemaRedocView,
    SchemaSwaggerView,
)

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # apps
    path('api/', include(('posts.urls', 'posts'), namespace='posts')),
    path('api/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('api/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    # open api
    path('api/schema/', SchemaAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SchemaRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/swagger-ui/', SchemaSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
