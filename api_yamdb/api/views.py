from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (
    IsAdminOrReadOnly, AdminModeratorAuthorPermission, AdminOnly
)
from api.serializers import (
    CategorySerializer, CommentSerializer, ReviewSerializer,
    GenreSerializer, SignUpSerializer, TokenSerializer,
    UserSerializer, TitleReadSerializer, TitleWriteSerializer
)
from reviews.models import Title, Category, Genre, Review

User = get_user_model()


class CategoryGenreBaseClass(
    viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Базовый класс для вьюсетов Категорий и Жанров.

    Проектом предусмотрено, что категории и жанры можно только просматривать,
    создавать и удалять. Создавать и удалять может только администратор
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)

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


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(CategoryGenreBaseClass):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseClass):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (AdminModeratorAuthorPermission,)

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
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (AdminModeratorAuthorPermission,)

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


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания пользователей."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def update_user(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Метод для регистрации пользователя."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Метод для получения токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get('username')
    )
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
