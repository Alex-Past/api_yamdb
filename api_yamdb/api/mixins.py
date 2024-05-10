from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAdminOrReadOnly


class CategoryGenreMixin(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
