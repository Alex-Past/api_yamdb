from rest_framework import filters, viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly
from api.serializers import CategorySerializer


class CategoryGenreMixin(
    viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Миксин для вьюсетов Категорий и Жанров.

    Проектом предусмотрено, что категории и жанры можно только просматривать,
    создавать и удалять. Создавать и удалять может только администратор
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination

    @action(
        methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug',
        detail=False
    )
    def get_genre_or_category(self, request, slug):
        genre_or_category = self.get_object()
        serializer = CategorySerializer(genre_or_category)
        genre_or_category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
