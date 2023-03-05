from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from core.shared.factories import ProfileFactory
from core.shared.unit_tests import APITestCase
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, ProfileListSerializer


class ProfileViewsTests(APITestCase):
    profiles_url = reverse_lazy('profiles:profiles-list')
    followed_url = reverse_lazy('profiles:profiles-followed')
    followers_url = reverse_lazy('profiles:profiles-followers')

    def test_list_profiles(self):
        profile = ProfileFactory()
        ProfileFactory.create_batch(5)
        expected_queryset = Profile.objects.all()
        self._require_jwt(profile.user)
        response = self.client.get(self.profiles_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], Profile.objects.count())
        self.assertEqual(
            response_json['results'],
            ProfileListSerializer(expected_queryset, many=True, user=profile.user).data
        )

    def test_list_profiles_unauthorized(self):
        ProfileFactory.create_batch(5)
        expected_queryset = Profile.objects.all()
        response = self.client.get(self.profiles_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], Profile.objects.count())
        self.assertEqual(
            response_json['results'],
            ProfileListSerializer(expected_queryset, many=True, user=AnonymousUser()).data
        )

    def test_list_profiles_filter_by_username(self):
        query = 'test'
        profile = ProfileFactory()
        ProfileFactory.create_batch(5)
        ProfileFactory.create(user__username='testowy')
        ProfileFactory.create(user__username='Testoviron')

        expected_queryset = Profile.objects.filter(user__username__icontains=query)

        self._require_jwt(profile.user)
        response = self.client.get(self.profiles_url, {'username': query})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(
            response_json['results'],
            ProfileListSerializer(expected_queryset, many=True, user=profile.user).data
        )

    def test_retrieve_profile(self):
        profile = ProfileFactory()
        self._require_jwt(profile.user)
        response = self.client.get(
            reverse_lazy('profiles:profiles-detail', kwargs={'username': profile.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), ProfileSerializer(profile, user=profile.user).data)

    def test_retrieve_profile_unauthorized(self):
        profile = ProfileFactory()
        response = self.client.get(
            reverse_lazy('profiles:profiles-detail', kwargs={'username': profile.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), ProfileSerializer(profile, user=AnonymousUser()).data)

    def test_retrieve_profile_does_not_exist(self):
        response = self.client.get(
            reverse_lazy('profiles:profiles-detail', kwargs={'username': 'testxddddddd'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_profile(self):
        profile1 = ProfileFactory()
        profile2 = ProfileFactory()
        self._require_jwt(profile1.user)
        response = self.client.post(
            reverse_lazy('profiles:profiles-follow', kwargs={'username': profile2.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), ProfileSerializer(profile2, user=profile1.user).data)
        self.assertTrue(profile1.is_following(profile2))
        self.assertTrue(profile2.is_followed_by(profile1))

    def test_follow_self(self):
        profile = ProfileFactory()
        self._require_jwt(profile.user)
        response = self.client.post(
            reverse_lazy('profiles:profiles-follow', kwargs={'username': profile.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('followee', response.json())

    def test_unfollow_profile(self):
        profile1 = ProfileFactory()
        profile2 = ProfileFactory()
        self._require_jwt(profile1.user)
        profile1.follow(profile2)
        self.assertTrue(profile1.is_following(profile2))
        self.assertTrue(profile2.is_followed_by(profile1))
        response = self.client.delete(
            reverse_lazy('profiles:profiles-follow', kwargs={'username': profile2.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), ProfileSerializer(profile2, user=profile1.user).data)
        self.assertFalse(profile1.is_following(profile2))
        self.assertFalse(profile2.is_followed_by(profile1))

    def test_unfollow_self(self):
        profile = ProfileFactory()
        self._require_jwt(profile.user)
        response = self.client.delete(
            reverse_lazy('profiles:profiles-follow', kwargs={'username': profile.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('followee', response.json())

    def test_list_followed_unauthorized(self):
        response = self.client.get(self.followed_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_followed(self):
        pass

    def test_list_followed_filter_by_username(self):
        pass

    def test_list_followers_unauthorized(self):
        response = self.client.get(self.followers_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_followers(self):
        pass

    def test_list_followers_filter_by_username(self):
        pass
