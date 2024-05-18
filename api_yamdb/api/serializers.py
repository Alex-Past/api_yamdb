from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, GenreTitle, Comment, Review
from consts import MAX_LEN_NAME, MAX_LEN_SLUG


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категория."""
    name = serializers.CharField(
        max_length=MAX_LEN_NAME,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=MAX_LEN_SLUG,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанр."""
    name = serializers.CharField(
        max_length=MAX_LEN_NAME,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=MAX_LEN_SLUG,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о произведении."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о произведении."""

    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = User
        


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать имя "me"')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)    

