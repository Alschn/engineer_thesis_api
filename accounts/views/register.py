from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from accounts.serializers import UserRegisterSerializer


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
