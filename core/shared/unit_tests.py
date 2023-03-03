from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from accounts.utils import get_tokens_for_user


class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def _require_jwt(self, user: User):
        access, _ = get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
