import time

from django.core.management import BaseCommand
from django.db import transaction

from accounts.models import User
from posts.models import Post, Comment, Tag
from profiles.models import Profile


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        start_time = time.perf_counter()

        self.stdout.write('Clearing tags...')
        tags_count, _ = Tag.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Cleared {tags_count} tags.\n'))

        self.stdout.write('Clearing comments...')
        comments_count, _ = Comment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Cleared {comments_count} comments.\n'))

        self.stdout.write('Clearing posts...')
        posts_count, _ = Post.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Cleared {posts_count} posts.\n'))

        self.stdout.write('Clearing profiles...')
        profiles_count, _ = Profile.objects.filter(user__is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS(f'Cleared {profiles_count} profiles.\n'))

        self.stdout.write('Clearing users...')
        users_count, _ = User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS(f'Cleared {users_count} users.\n'))

        end_time = time.perf_counter()
        self.stdout.write(
            self.style.SUCCESS(f'Done in {end_time - start_time:.2f} seconds.')
        )
