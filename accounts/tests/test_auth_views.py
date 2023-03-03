import random
import string

from rest_framework import status
from rest_framework.reverse import reverse_lazy

from accounts.models import User
from accounts.serializers import UserRegisterSerializer
from accounts.utils import get_tokens_for_user
from core.shared.factories import UserFactory, DEFAULT_USER_FACTORY_PASSWORD
from core.shared.unit_tests import APITestCase


class AuthViewsTests(APITestCase):
    token_url = reverse_lazy('accounts:token_obtain_pair')
    token_refresh_url = reverse_lazy('accounts:token_refresh')
    token_verify_url = reverse_lazy('accounts:token_verify')
    register_url = reverse_lazy('accounts:register')

    @classmethod
    def setUpTestData(cls):
        cls.user: User = UserFactory(email='test@example.com')

    def test_obtain_token(self):
        response = self.client.post(self.token_url, {
            'email': self.user.email,
            'password': DEFAULT_USER_FACTORY_PASSWORD
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_json)
        self.assertIn('refresh', response_json)

    def test_obtain_token_user_not_found(self):
        response = self.client.post(self.token_url, {
            'email': 'test_email@example.com',
            'password': 'test_password'
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_json)

    def test_obtain_token_missing_fields(self):
        response = self.client.post(self.token_url, {})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response_json)
        self.assertIn('password', response_json)

    def test_refresh_token(self):
        _, refresh = get_tokens_for_user(self.user)
        response = self.client.post(self.token_refresh_url, {
            'refresh': refresh
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_json)
        self.assertNotIn('refresh', response_json)

    def test_refresh_token_invalid_type(self):
        access, _ = get_tokens_for_user(self.user)
        response = self.client.post(self.token_refresh_url, {
            'refresh': access
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_json)
        self.assertIn('code', response_json)

    def test_refresh_token_with_invalid_token(self):
        response = self.client.post(self.token_refresh_url, {
            'refresh': 'test.test.test'
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_json)
        self.assertIn('code', response_json)

    def test_verify_token(self):
        _, refresh = get_tokens_for_user(self.user)
        response = self.client.post(self.token_verify_url, {
            'refresh': refresh
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token_with_invalid_token(self):
        response = self.client.post(self.token_verify_url, {
            'refresh': 'test.test.test'
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_json)
        self.assertIn('code', response_json)

    def test_verify_token_wrong_type(self):
        access, _ = get_tokens_for_user(self.user)
        response = self.client.post(self.token_verify_url, {
            'refresh': access
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_json)
        self.assertIn('code', response_json)

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'email': 'new@example.com',
            'username': 'new_user_123',
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        user = User.objects.get(email="new@example.com")
        self.assertIsNotNone(user.profile)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), UserRegisterSerializer(instance=user).data)

    def test_register_user_email_already_taken(self):
        response = self.client.post(self.register_url, {
            'email': self.user.email,
            'username': 'test_user',
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())

    def test_register_user_username_already_taken(self):
        response = self.client.post(self.register_url, {
            'email': 'testowy@example.com',
            'username': self.user.username,
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json())

    def test_register_user_username_email_already_taken(self):
        response = self.client.post(self.register_url, {
            'email': self.user.email,
            'username': self.user.username,
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())
        self.assertIn('username', response.json())

    def test_register_user_passwords_do_not_match(self):
        response = self.client.post(self.register_url, {
            'email': 'new@example.com',
            'username': 'new_user_123',
            'password1': 'test_password_123',
            'password2': 'test_password_1234'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.json())

    def test_register_user_passwords_too_weak(self):
        response = self.client.post(self.register_url, {
            'email': 'new@example.com',
            'username': 'new_user_123',
            'password1': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.json())

    def test_register_user_username_too_short(self):
        response = self.client.post(self.register_url, {
            'email': 'new@example.com',
            'username': ''.join(random.choices(string.ascii_lowercase, k=2)),
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json())

    def test_register_user_username_too_long(self):
        response = self.client.post(self.register_url, {
            'email': 'new@example.com',
            'username': ''.join(random.choices(string.ascii_lowercase, k=31)),
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json())

    def test_register_user_email_missing(self):
        response = self.client.post(self.register_url, {
            'username': 'new_user',
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())

    def test_register_username_missing(self):
        response = self.client.post(self.register_url, {
            'email': 'new@example.com',
            'password1': 'test_password_123',
            'password2': 'test_password_123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json())
