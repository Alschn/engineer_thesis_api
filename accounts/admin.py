from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin as BaseOutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from profiles.admin import InlineProfileAdmin

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff')
    list_filter = ('is_superuser', 'is_active')
    inlines = (InlineProfileAdmin,)


class OutstandingTokenAdmin(BaseOutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return True


admin.site.unregister([Group])

admin.site.register(User, UserAdmin)

admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
