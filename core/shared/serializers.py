from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from rest_framework.serializers import Serializer

from accounts.models import User


class UserAttributeRequiredError(AttributeError):
    pass


class ToRepresentationRequiresUserMixin:
    """
    Mixin required for serializers whose some fields are of Serializer type,
    that require either `user` or context['request'] present in them.
    In normal circumstances, children serializers have their parent's context by default.


    Example:
        class PostSerializer(serializers.ModelSerializer):
            author = ProfileSerializer()    # <- this needs user attribute or request in context

            ...

        class ProfileSerializer(serializers.ModelSerializer):
            ...

            def get_is_following(self, instance: Profile) -> bool:
                user = self.user or self.context['request'].user
                ...

    # If we want to test serializer whose children need `user` or `context['request']`, they will not be able to get it.

    Use case:
        class Tests(TestCase):
            def test_something(self):
                current_user = UserFactory()
                post = PostFactory(author=current_user)
                self.require_auth(current_user)
                serializer = PostSerializer(post, user=user)
                ...
                self.assertEqual(response.json(), serializer.data)

    Solution:
        class PostSerializer(ToRepresentationRequiresUserMixin, serializers.ModelSerializer):
            author = ProfileSerializer()

        ... # same as above
    """

    user_attr = 'user'

    _readable_fields: list
    context: dict

    def __init__(self, *args, user: User | AnonymousUser = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                # ---CUSTOM PART---
                # We need to pass the user to the related serializer
                # so that its to_representation does not throw an error
                if isinstance(field, Serializer):
                    error_message = (
                        f"{self.__class__.__name__} must either: \n"
                        f"1. Include a `user` attribute, \n"
                        f"2. Include a `context['request']` attribute, \n"
                        f"To serialize '{field.field_name}' field with `{field.__class__.__name__}`."
                    )

                    if not getattr(self, 'user', None) and not self.context.get('request'):
                        raise UserAttributeRequiredError(error_message)

                    elif getattr(self, 'user', None) is not None:
                        field.user = self.user

                    elif self.context.get('request') is not None:
                        field.context['request'] = self.context['request']

                    else:
                        raise UserAttributeRequiredError(error_message)
                # ---CUSTOM PART ENDS HERE---

                ret[field.field_name] = field.to_representation(attribute)

        return ret
