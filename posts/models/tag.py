from django.db import models

from core.shared.models import TimestampedModel


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self) -> str:
        return self.tag
