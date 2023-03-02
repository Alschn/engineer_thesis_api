from rest_framework_simplejwt.views import TokenRefreshView

from accounts.serializers.auth import TokenRefreshSerializer


class JWTRefreshView(TokenRefreshView):
    """
    POST /api/auth/token/refresh/
    """
    serializer_class = TokenRefreshSerializer
