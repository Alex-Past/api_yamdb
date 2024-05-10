from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права администратора (Title, Category, Genre)."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Разрешение для автора на редактирование и удаления (Review, Comment, оценка)."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsModerator(IsAuthorOrReadOnly):
    """Разрешение для модератора на редактирование и удаления (Review, Comment, оценка)."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator
