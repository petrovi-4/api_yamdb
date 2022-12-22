from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
            or request.method in permissions.SAFE_METHODS
        )


class IsAuthorOrModeratorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_admin or user.is_staff or user.is_moderator or user == obj.author
