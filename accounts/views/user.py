from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserSerializer
from accounts.serializers.user import UserUpdateSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer

        return UserUpdateSerializer

    # TODO:

    def retrieve(self, request, *args, **kwargs):
        raise NotImplementedError

    def update(self, request, *args, **kwargs):
        raise NotImplementedError
