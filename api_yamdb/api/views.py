from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg

from api.serializers import TitleSerializer, CategorySerializer, \
    GenreSerializer
from reviews.models import Title, Category, Genre


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    # related_name="reviews" в модели Review
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    # Жду прав доступа
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = (
        'category__slug_cat', 'genres__slug_genre', 'name', 'year'
    )


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    # Жду прав доступа
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ('name_cat',)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    # Жду прав доступа
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ('name_genre',)
