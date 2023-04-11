from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from core.shared.factories import ProfileFactory, TagFactory, PostFactory, CommentFactory, UserFactory
from core.shared.unit_tests import APITestCase, TearDownFilesMixin
from posts.models import Post
from posts.serializers import PostSerializer
from posts.serializers.comment import EmbeddedCommentSerializer
from posts.serializers.post import PostListSerializer, PostUpdateSerializer

BASE_64_HEADER = 'data:image/png;base64'
BASE_64_PAYLOAD = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAEElEQVR4nGLacJwDEAAA//8DsgGCR4reaAAAAABJRU5ErkJggg=='
BASE_64_IMAGE = f'{BASE_64_HEADER},{BASE_64_PAYLOAD}'


class PostsViewsTests(TearDownFilesMixin, APITestCase):
    posts_url = reverse_lazy('posts:posts-list')

    def test_list_posts(self):
        profile = ProfileFactory()
        PostFactory.create_batch(10)
        expected_queryset = Post.objects.all()
        self._require_jwt(profile.user)
        response = self.client.get(self.posts_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(response_json['results'], PostListSerializer(
            expected_queryset, many=True, user=profile.user
        ).data)

    def test_list_posts_unauthorized(self):
        PostFactory.create_batch(10)
        expected_queryset = Post.objects.all()
        response = self.client.get(self.posts_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(response_json['results'], PostListSerializer(
            expected_queryset, many=True, user=AnonymousUser()
        ).data)

    # todo: filtering, ordering, searching, etc.

    def test_list_feed_posts(self):
        profile = ProfileFactory()
        followed = ProfileFactory.create_batch(10)
        profile.followed.set(followed)
        for author in followed:
            PostFactory(author=author)

        expected_queryset = Post.objects.filter(author__in=followed)

        self._require_jwt(profile.user)
        response = self.client.get(reverse_lazy('posts:posts-feed'))
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(response_json['results'], PostListSerializer(
            expected_queryset, many=True, user=profile.user
        ).data)

    def test_list_feed_posts_unauthorized(self):
        response = self.client.get(reverse_lazy('posts:posts-feed'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_favourites_posts(self):
        profile = ProfileFactory()
        posts = PostFactory.create_batch(10)
        profile.favourites.set(posts)

        expected_queryset = profile.favourites.all()

        self._require_jwt(profile.user)
        response = self.client.get(reverse_lazy('posts:posts-favourites'))
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(response_json['results'], PostListSerializer(
            expected_queryset, many=True, user=profile.user
        ).data)

    def test_list_favourites_posts_unauthorized(self):
        response = self.client.get(reverse_lazy('posts:posts-favourites'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post(self):
        profile = ProfileFactory()
        self._require_jwt(profile.user)

        response = self.client.post(self.posts_url, {
            'title': 'Test title',
            'description': 'Test description',
            'body': 'Test body',
            'tags': ['test', 'test1'],
            'thumbnail': BASE_64_IMAGE
        })
        post = profile.posts.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.tags.count(), 2)

    def test_create_post_unauthorized(self):
        response = self.client.post(self.posts_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_invalid_data(self):
        profile = ProfileFactory()
        self._require_jwt(profile.user)

        response = self.client.post(self.posts_url, {
            'title': '',
            'description': '',
            'body': '',
            'tags': [],
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response_json)
        self.assertIn('description', response_json)
        self.assertIn('body', response_json)
        self.assertIn('tags', response_json)
        self.assertIn('thumbnail', response_json)

    def test_create_post_existing_tags(self):
        profile = ProfileFactory()
        self._require_jwt(profile.user)

        tag = TagFactory()

        response = self.client.post(self.posts_url, {
            'title': 'Test title',
            'description': 'Test description',
            'body': 'Test body',
            'tags': [tag.tag],
            'thumbnail': BASE_64_IMAGE
        })
        post = profile.posts.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.tags.count(), 1)

    def test_retrieve_post(self):
        post = PostFactory(tags=True, comments=True)
        profile = post.author
        self._require_jwt(profile.user)

        response = self.client.get(reverse_lazy('posts:posts-detail', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), PostSerializer(post, user=profile.user).data)

    def test_retrieve_post_unauthorized(self):
        post = PostFactory()
        profile = post.author
        self._require_jwt(profile.user)

        response = self.client.get(reverse_lazy('posts:posts-detail', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), PostSerializer(post, user=profile.user).data)

    def test_retrieve_post_not_found(self):
        response = self.client.get(reverse_lazy('posts:posts-detail', args=('test',)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_post_to_favourites(self):
        profile = ProfileFactory()
        post = PostFactory()

        self._require_jwt(profile.user)

        response = self.client.post(reverse_lazy('posts:posts-favourite', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.favourites.count(), 1)

    def test_add_post_to_favourites_unauthorized(self):
        post = PostFactory()
        response = self.client.post(reverse_lazy('posts:posts-favourite', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_post_to_favourites_not_found(self):
        user = UserFactory()
        self._require_jwt(user)
        response = self.client.post(reverse_lazy('posts:posts-favourite', args=('testttttt',)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_post_already_in_favourites(self):
        profile = ProfileFactory()
        post = PostFactory()

        profile.favourites.add(post)
        self.assertEqual(profile.favourites.count(), 1)

        self._require_jwt(profile.user)

        response = self.client.post(reverse_lazy('posts:posts-favourite', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.favourites.count(), 1)

    def test_remove_post_from_favourites(self):
        profile = ProfileFactory()
        post = PostFactory()

        profile.favourites.add(post)
        self.assertEqual(profile.favourites.count(), 1)

        self._require_jwt(profile.user)

        response = self.client.delete(reverse_lazy('posts:posts-favourite', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.favourites.count(), 0)

    def test_remove_post_from_favourites_unauthorized(self):
        post = PostFactory()
        response = self.client.delete(reverse_lazy('posts:posts-favourite', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_post_from_favourites_not_found(self):
        user = UserFactory()
        self._require_jwt(user)
        response = self.client.delete(reverse_lazy('posts:posts-favourite', args=('testttttt',)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_post_not_in_favourites(self):
        profile = ProfileFactory()
        post = PostFactory()

        self.assertEqual(profile.favourites.count(), 0)

        self._require_jwt(profile.user)

        response = self.client.delete(reverse_lazy('posts:posts-favourite', args=(post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.favourites.count(), 0)

    def test_post_list_comments(self):
        post = PostFactory(comments=True)
        profile = post.author
        self._require_jwt(profile.user)

        response = self.client.get(reverse_lazy('posts:posts-comments', args=(post.slug,)))
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], post.comments.count())
        self.assertEqual(response_json['results'], EmbeddedCommentSerializer(
            post.comments, many=True, user=profile.user
        ).data)

    def test_post_retrieve_comment(self):
        post = PostFactory(comments=True, comments__size=1)
        comment = post.comments.first()
        profile = post.author
        self._require_jwt(profile.user)

        response = self.client.get(reverse_lazy('posts:posts-comments-detail', args=(post.slug, comment.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), EmbeddedCommentSerializer(comment, user=profile.user).data)

    def test_post_delete_comment(self):
        post = PostFactory()
        profile = post.author
        comment = CommentFactory(author=profile, post=post)
        self._require_jwt(profile.user)
        response = self.client.delete(reverse_lazy('posts:posts-comments-detail', args=(post.slug, comment.id)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_delete_comment_not_author(self):
        post = PostFactory(comments=True, comments__size=1)
        comment = post.comments.first()
        profile = post.author
        self._require_jwt(profile.user)

        response = self.client.delete(reverse_lazy('posts:posts-comments-detail', args=(post.slug, comment.id)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post(self):
        post = PostFactory()
        profile = post.author

        self._require_jwt(profile.user)

        response = self.client.patch(reverse_lazy('posts:posts-detail', args=(post.slug,)), data={
            'description': 'test'
        })
        updated_post = Post.objects.get(slug=post.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), PostUpdateSerializer(instance=updated_post).data)

    def test_update_post_not_author(self):
        post = PostFactory()
        profile = ProfileFactory()

        self._require_jwt(profile.user)

        response = self.client.patch(reverse_lazy('posts:posts-detail', args=(post.slug,)), data={
            'description': 'test',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
