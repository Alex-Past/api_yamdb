from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg

from api.serializers import TitleSerializer
from reviews.models import Title


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
