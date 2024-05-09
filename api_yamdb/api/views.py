from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import TitleSerializer
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    # Жду прав доступа
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = (
        'category__slug_cat', 'genres__slug_genre', 'name', 'year'
    )
