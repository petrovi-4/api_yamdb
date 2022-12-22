from rest_framework.permissions import BasePermission
from rest_framework import permissions


class SafeOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        safe_request = request.method in permissions.SAFE_METHODS
        safe_user = request.user.is_admin or request.user.is_staff
        return safe_request or safe_user


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_staff


class IsAuthorOrModeratorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_admin or user.is_staff or user.is_moderator or user == obj.author
