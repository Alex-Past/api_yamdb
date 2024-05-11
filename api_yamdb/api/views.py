from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import send_mail
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.mixins import CategoryGenreMixin
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly, IsModerator, AdminModeratorAuthorPermission
from api.serializers import (
    CategorySerializer, CommentSerializer, ReviewSerializer,
    GenreSerializer, SignUpSerializer, TokenSerializer,
    UserSerializer, TitleReadSerializer, TitleWriteSerializer
)
from api.filters import TitleFilter

from reviews.models import Title, Category, Genre, Review

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(CategoryGenreMixin):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)


class GenreViewSet(CategoryGenreMixin):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

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
    serializer_class = ReviewSerializer

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
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=(IsAuthorOrReadOnly,),
            detail=False,
        )
    def create_user(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(subject='Регистрация на сайте api_yamdb',
                  message=f'Проверочный код: {confirmation_code}',
                  from_email='api_yamdb',
                  recipient_list=[email],
                  fail_silently=True,)

        return Response(serializer.data, status=status.HTTP_200_OK)    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=serializer.validated_data.get('username'))
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                