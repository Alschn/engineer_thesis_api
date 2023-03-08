from django.urls import path

from .views import (
    UserRetrieveUpdateAPIView,
    JWTObtainPairView,
    JWTRefreshView,
    JWTVerifyView,
    UserRegisterAPIView,
    LogoutView
)

urlpatterns = [
    path('users/me/', UserRetrieveUpdateAPIView.as_view(), name='users-me'),
    path('auth/token/', JWTObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', JWTRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', JWTVerifyView.as_view(), name='token_verify'),
    path('auth/register/', UserRegisterAPIView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
