import shutil

from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from accounts.models import User
from accounts.utils import get_tokens_for_user

TEST_DIR = settings.BASE_DIR / 'test_files'


class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def _require_jwt(self, user: User):
        access, _ = get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')


@override_settings(MEDIA_ROOT=TEST_DIR)
class TearDownFilesMixin(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        print(f"\n{cls.__name__}: Deleting temporary files...\n")
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print(f"\n{cls.__name__}: Failed to delete temporary files directory...\n")
