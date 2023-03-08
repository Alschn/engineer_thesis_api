from django import forms
from django.contrib import admin
from martor.widgets import AdminMartorWidget

from posts.models import Tag, Comment, Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': AdminMartorWidget,
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    form = PostAdminForm


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
