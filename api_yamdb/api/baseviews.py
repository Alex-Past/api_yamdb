from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAdminOrReadOnly


class CategoryGenreBaseViewSet(
    viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Базовый вьюсет для Категорий и Жанров.

    Проектом предусмотрено, что категории и жанры можно только просматривать,
    создавать и удалять. Создавать и удалять может только администратор
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
