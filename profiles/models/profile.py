from django.db import models

from core.shared.models import TimestampedModel
from posts.models import Post


class Profile(TimestampedModel):
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    followed = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )
    favourites = models.ManyToManyField(
        'posts.Post',
        related_name='favourited_by',
        blank=True
    )

    def __str__(self) -> str:
        return self.user.username

    def follow(self, profile: 'Profile') -> None:
        self.followed.add(profile)

    def unfollow(self, profile: 'Profile') -> None:
        self.followed.remove(profile)

    def is_following(self, profile: 'Profile') -> bool:
        return self.followed.contains(profile)

    def is_followed_by(self, profile: 'Profile') -> bool:
        return self.followers.contains(profile)

    def add_to_favourites(self, post: 'Profile') -> None:
        self.favourites.add(post)

    def remove_from_favourites(self, post: Post) -> None:
        self.favourites.remove(post)

    def added_to_favourites(self, post: Post) -> bool:
        return self.favourites.contains(post)
