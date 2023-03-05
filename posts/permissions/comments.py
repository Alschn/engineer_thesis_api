from typing import Any

from rest_framework import permissions
from rest_framework.request import Request

from posts.models import Comment


class IsCommentsAuthorPermission(permissions.BasePermission):
    protected_methods = ('PATCH', 'DELETE')

    def has_object_permission(self, request: Request, view: Any, obj: Comment) -> bool:
        if request.method in self.protected_methods:
            return request.user.is_authenticated and obj.author == request.user.profile

        return True
