"""YaMDb permissions"""
from rest_framework import permissions


def is_admin(request):
    """Админ или модератор"""
    admin_roles = ('moderator', 'admin')
    user = request.user
    result = user.is_authenticated and user.role in admin_roles
    return result


class CustomAdminPermission(permissions.BasePermission):
    """Кастомный пермишн модератора и администратора"""

    def has_permission(self, request, view):
        safe_request = request.method in permissions.SAFE_METHODS
        return safe_request or is_admin(request)

    def has_object_permission(self, request, view, obj):
        safe_request = request.method in permissions.SAFE_METHODS
        return safe_request or is_admin(request)
