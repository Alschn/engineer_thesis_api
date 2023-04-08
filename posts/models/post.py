from django.db import models

from core.shared.models import TimestampedModel


class Post(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    body = models.TextField()
    is_published = models.BooleanField(db_index=True, default=True)
    thumbnail = models.ImageField(upload_to='posts/thumbnails', null=True, blank=True)
    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    tags = models.ManyToManyField(
        'posts.Tag',
        related_name='posts'
    )

    def __str__(self) -> str:
        return self.slug

    @property
    def favourites_count(self) -> int:
        return self.favourited_by.count()

    @property
    def comments_count(self) -> int:
        return self.comments.count()
