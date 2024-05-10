from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from api.serializers import TitleSerializer, CategorySerializer, CommentSerializer, ReviewSerializer, GenreSerializer
from reviews.models import Title, Category, Genre, Review


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = #Пермишшены моделей автора, модератора или админа

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = #пермишн модели автора, модератора или админа

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)