from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права администратора (Title, Category, Genre)."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """Резрешение для админа/модератора/автора на различные действия."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class AdminOnly(permissions.BasePermission):
    """Резрешение для админа на различные действия."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Уже было прописано выше, но на всякий случай"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
