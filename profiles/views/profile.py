from typing import Any

from django.db.models import QuerySet
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.shared.pagination import page_number_pagination_factory
from profiles.filters.profile import ProfilesFilterSet
from profiles.models import Profile
from profiles.serializers import (
    ProfileSerializer,
    ProfileListSerializer
)

ProfilesPagination = page_number_pagination_factory(
    page_size=25,
    max_page_size=100
)


class ProfilesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    GET     /api/profiles/

    GET     /api/profiles/<str:username>/

    POST    /api/profiles/<str:username>/follow/

    DELETE  /api/profiles/<str:username>/follow/
    """
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
    filterset_class = ProfilesFilterSet
    pagination_class = ProfilesPagination
    lookup_url_kwarg = 'username'
    lookup_field = 'user__username'

    def get_queryset(self) -> QuerySet[Profile]:
        if self.action == "followed":
            return self.request.user.profile.followed.prefetch_related('user')

        elif self.action == "followers":
            return self.request.user.profile.followers.prefetch_related('user')

        return Profile.objects.select_related('user')

    def get_serializer_class(self):
        if self.action in ["list", "followers", "followed"]:
            return ProfileListSerializer

        return super().get_serializer_class()

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_name='follow', url_path='follow',
        permission_classes=[IsAuthenticated]
    )
    def follow(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        follower = request.user.profile
        followee = self.get_object()

        if follower.pk == followee.pk:
            return Response({'followee': 'You cannot follow/unfollow yourself!'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            follower.follow(followee)
        else:
            follower.unfollow(followee)

        serializer = self.get_serializer(followee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['GET'], detail=False,
        url_name='followed', url_path='followed',
        permission_classes=[IsAuthenticated]
    )
    def followed(self, *args: Any, **kwargs: Any):
        return super().list(self, *args, **kwargs)

    @action(
        methods=['GET'], detail=False,
        url_name='followers', url_path='followers',
        permission_classes=[IsAuthenticated]
    )
    def followers(self, *args: Any, **kwargs: Any):
        return super().list(self, *args, **kwargs)
