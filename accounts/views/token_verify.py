from rest_framework_simplejwt.views import TokenVerifyView

from accounts.serializers.auth import TokenRefreshSerializer


class JWTVerifyView(TokenVerifyView):
    """
    POST /api/auth/token/verify/
    """
    serializer_class = TokenRefreshSerializer
