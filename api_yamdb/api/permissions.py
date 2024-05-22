from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права администратора (Title, Category, Genre)."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class AdminModeratorAuthorPermission(permissions.IsAuthenticatedOrReadOnly):
    """Резрешение для админа/модератора/автора на различные действия."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
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
