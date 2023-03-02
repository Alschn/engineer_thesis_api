from django.contrib import admin

from profiles.models import Profile


class InlineProfileAdmin(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    list_select_related = ('user',)
    search_fields = ('user__username',)
