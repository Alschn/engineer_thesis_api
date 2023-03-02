from django.db import models

from core.shared.models import TimestampedModel


class Comment(TimestampedModel):
    body = models.TextField()
    post = models.ForeignKey(
        'posts.Post',
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'profiles.Profile',
        related_name='comments',
        on_delete=models.CASCADE
    )
