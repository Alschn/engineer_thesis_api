import random
from collections.abc import Iterable
from typing import Any

import factory
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from factory import Faker
from factory.django import DjangoModelFactory
from mdgen import MarkdownPostProvider

from posts.models import Post

DEFAULT_USER_FACTORY_PASSWORD = 'test'

Faker.add_provider(MarkdownPostProvider)


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(
        lambda o: "%s_%s" % (o.first_name.lower(), o.last_name.lower())
    )
    email = factory.LazyAttribute(
        lambda o: "%s.%s@example.com" % (o.first_name.lower(), o.last_name.lower())
    )
    is_active = True
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_USER_FACTORY_PASSWORD)
    profile = factory.RelatedFactory(
        'core.shared.factories.ProfileFactory',
        factory_related_name='user'
    )


@factory.django.mute_signals(post_save)
class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = 'profiles.Profile'

    user = factory.SubFactory(
        'core.shared.factories.UserFactory',
        profile=None
    )
    bio = factory.Faker('text', max_nb_chars=200)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = 'posts.Post'

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text', max_nb_chars=200)
    body = factory.Faker(
        'post',
        size=factory.LazyFunction(
            lambda: random.choice(['small', 'medium'])
        )
    )
    author = factory.SubFactory(
        'core.shared.factories.ProfileFactory',
    )

    @factory.post_generation
    def slug(obj: Post, created: bool, extracted: Any, **kwargs: Any):
        if not created:
            return

        random_string = get_random_string(length=6)
        slug = slugify(f'{obj.title}-{random_string}')
        obj.slug = extracted or slug

    @factory.post_generation
    def tags(obj: Post, created: bool, extracted: Any, **kwargs: Any):
        if not created:
            return

        size = kwargs.pop('size', None)

        if isinstance(extracted, bool) and extracted is True:
            tags = TagFactory.create_batch(
                size=size or random.randint(1, 3),
                **kwargs,
            )
            obj.tags.add(*tags)

        elif isinstance(extracted, Iterable):
            obj.tags.add(*extracted)

    @factory.post_generation
    def comments(obj: Post, created: bool, extracted: Any, **kwargs: Any):
        if not created:
            return

        size = kwargs.pop('size', None)

        if isinstance(extracted, bool) and extracted is True:
            CommentFactory.create_batch(
                size=size or random.randint(1, 4),
                post=obj,
                **kwargs,
            )


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = 'posts.Comment'

    body = factory.Faker('text', max_nb_chars=100)
    post = factory.SubFactory(
        'core.shared.factories.PostFactory',
    )
    author = factory.SubFactory(
        'core.shared.factories.ProfileFactory',
    )


class TagFactory(DjangoModelFactory):
    class Meta:
        model = 'posts.Tag'

    tag = factory.Faker('word')

    @factory.post_generation
    def slug(obj, create, extracted, **kwargs):
        if not create:
            return

        random_string = get_random_string(length=6)
        slug = slugify(f'{obj.tag}-{random_string}')
        obj.slug = extracted or slug
