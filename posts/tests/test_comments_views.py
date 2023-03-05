from rest_framework import status
from rest_framework.reverse import reverse_lazy

from core.shared.factories import PostFactory, UserFactory
from core.shared.unit_tests import APITestCase
from posts.models import Comment
from posts.serializers import CommentSerializer


class CommentsViewsTests(APITestCase):
    comments_url = reverse_lazy("posts:comments-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_list_comments(self):
        self._require_jwt(self.user)
        PostFactory(comments=True, comments__size=10)
        expected_queryset = Comment.objects.all()
        response = self.client.get(self.comments_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(response_json['results'], CommentSerializer(expected_queryset, many=True).data)

    def test_list_comments_filter_by_author(self):
        self._require_jwt(self.user)
        PostFactory(comments=True, comments__size=5)
        PostFactory(comments=True, comments__size=5, comments__author=self.user.profile)
        expected_queryset = Comment.objects.filter(author=self.user.profile)
        response = self.client.get(self.comments_url, data={
            "author": self.user.profile.id
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(response_json['results'], CommentSerializer(expected_queryset, many=True).data)

    def test_list_comments_filter_by_post(self):
        pass

    def test_list_comments_filter_by_post_title(self):
        pass

    def test_create_comment(self):
        self._require_jwt(self.user)
        post = PostFactory()
        response = self.client.post(self.comments_url, data={
            "body": "Test comment",
            "post": post.slug
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.comments.count(), 1)

    def test_create_comment_empty(self):
        self._require_jwt(self.user)
        post = PostFactory()
        response = self.client.post(self.comments_url, data={
            "body": "",
            "post": post.slug
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("body", response.json())

    def test_create_comment_post_does_not_exist(self):
        self._require_jwt(self.user)
        response = self.client.post(self.comments_url, data={
            "body": "",
            "post": 1000
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("post", response.json())
