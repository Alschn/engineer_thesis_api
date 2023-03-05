from django.test import TestCase

from core.shared.factories import ProfileFactory, PostFactory


class ProfileModelTests(TestCase):

    def test_to_string(self):
        profile = ProfileFactory()
        self.assertEqual(str(profile), profile.user.username)

    def test_follow(self):
        profile1 = ProfileFactory()
        profile2 = ProfileFactory()
        profile1.follow(profile2)
        self.assertTrue(profile2.is_followed_by(profile1))
        self.assertTrue(profile1.is_following(profile2))

    def test_follow_already_followed(self):
        profile1 = ProfileFactory()
        profile2 = ProfileFactory()

        profile2.followers.add(profile1)
        self.assertTrue(profile2.is_followed_by(profile1))
        self.assertTrue(profile1.is_following(profile2))

        profile1.follow(profile2)
        self.assertTrue(profile2.is_followed_by(profile1))
        self.assertTrue(profile1.is_following(profile2))

    def test_follow_self(self):
        profile = ProfileFactory()
        profile.follow(profile)
        self.assertTrue(profile.is_following(profile))

    def test_unfollow(self):
        profile1 = ProfileFactory()
        profile2 = ProfileFactory()
        profile1.followed.add(profile2)

        self.assertTrue(profile2.is_followed_by(profile1))

        profile1.unfollow(profile2)

        self.assertFalse(profile2.is_followed_by(profile1))

    def test_unfollow_not_followed(self):
        profile1 = ProfileFactory()
        profile2 = ProfileFactory()
        self.assertFalse(profile1.is_following(profile2))
        profile1.unfollow(profile2)
        self.assertFalse(profile1.is_following(profile2))

    def test_unfollow_self(self):
        profile = ProfileFactory()
        profile.follow(profile)
        self.assertTrue(profile.is_following(profile))
        profile.unfollow(profile)
        self.assertFalse(profile.is_following(profile))

    def test_is_following_self(self):
        profile = ProfileFactory()
        self.assertFalse(profile.is_following(profile))

    def test_is_followed_by_self(self):
        profile = ProfileFactory()
        self.assertFalse(profile.is_followed_by(profile))

    def test_add_to_favourites(self):
        profile = ProfileFactory()
        post = PostFactory()
        self.assertFalse(profile.added_to_favourites(post))
        profile.add_to_favourites(post)
        self.assertTrue(profile.added_to_favourites(post))

    def test_add_to_favourites_already_favourited(self):
        profile = ProfileFactory()
        post = PostFactory()
        post.favourited_by.add(profile)
        self.assertTrue(profile.added_to_favourites(post))
        profile.add_to_favourites(post)
        self.assertTrue(profile.added_to_favourites(post))

    def test_remove_from_favourites(self):
        profile = ProfileFactory()
        post = PostFactory()
        post.favourited_by.add(profile)
        self.assertTrue(profile.added_to_favourites(post))
        profile.remove_from_favourites(post)
        self.assertFalse(profile.added_to_favourites(post))

    def test_remove_from_favourites_not_favourited(self):
        profile = ProfileFactory()
        post = PostFactory()
        self.assertFalse(profile.added_to_favourites(post))
        profile.remove_from_favourites(post)
        self.assertFalse(profile.added_to_favourites(post))
