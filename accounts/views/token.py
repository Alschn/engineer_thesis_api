from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers.auth import TokenObtainPairSerializer


class JWTObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/token/
    """
    serializer_class = TokenObtainPairSerializer
