from typing import Any

from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Profile
from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender: ModelBase, instance: User, created: bool, *args: Any, **kwargs: Any) -> None:
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
