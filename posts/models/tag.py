import secrets
from colorfield.fields import ColorField
from django.db import models

from core.shared.models import TimestampedModel


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)
    color = ColorField(default='#000000', blank=True, null=True)

    def save(self, *args, **kwargs) -> None:
        if not self.color:
            self.color = f'#{secrets.token_hex(3)}'

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.tag
