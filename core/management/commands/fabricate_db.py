import time

from django.core.management import BaseCommand, CommandParser
from django.db import transaction

from accounts.models import User
from core.shared.factories import UserFactory, PostFactory
from posts.models import Post
from profiles.models import Profile

DEFAULT_POSTS_COUNT = 10


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--posts',
            type=int,
            default=DEFAULT_POSTS_COUNT,
            help='Number of posts to fabricate',
        )

    def handle(self, *args, **options):
        posts_count = options['posts']

        start_time = time.perf_counter()

        try:
            with transaction.atomic():
                user, profile = fabricate_test_user()

                posts = fabricate_posts_for_profile(profile, count=posts_count)

                self.stdout.write(
                    self.style.SUCCESS(f'Done in {time.perf_counter() - start_time:.2f} seconds.')
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR('\nERROR: Rolling back...'))
            raise e


def fabricate_test_user(email: str = "test@example.com", username: str = "test") -> tuple[User, Profile]:
    user = User.objects.filter(email=email).first()
    if not user:
        user = UserFactory(username=username, email="test@example.com")
        user.set_password('test')
    else:
        print(f'User {user} already exists, skipping creation...')
        user.username = username

    user.save()
    profile = user.profile
    return user, profile


def fabricate_posts_for_profile(
        profile: Profile, *,
        count: int = DEFAULT_POSTS_COUNT,
        **kwargs
) -> list[Post]:
    posts = PostFactory.create_batch(
        count,
        author=profile,
        tags=True,
        comments=True,
        **kwargs
    )
    return posts
