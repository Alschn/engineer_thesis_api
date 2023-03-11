import django_filters.filters as filters
from django_filters.rest_framework import FilterSet

from profiles.models import Profile


class ProfilesFilterSet(FilterSet):
    username = filters.CharFilter(
        field_name='user__username',
        lookup_expr='iexact'
    )
    username__icontains = filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains',
    )

    class Meta:
        model = Profile
        fields = [
            'username',
        ]
