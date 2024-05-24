from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import MAX_LEN_EMAIL, MAX_LEN_NAME
from users.validators import username_validator
from reviews.models import Category, Genre, Title, Comment, Review

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категория."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанр."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о произведении."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о произведении."""

    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
        allow_null=False, allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментарии."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        exclude = ('review',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывы."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
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
        exclude = ('title',)
        model = Review


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        validators=[username_validator,],
        max_length=MAX_LEN_NAME,
        required=True
    )
    email = serializers.EmailField(max_length=MAX_LEN_EMAIL, required=True)

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        try:
            user, create = User.objects.get_or_create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': f'пользователь с именем "{username}" '
                 f'или почтой "{email}" уже существует'}
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(subject='Регистрация на сайте api_yamdb',
                  message=f'Проверочный код: {confirmation_code}',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  fail_silently=True, )
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для использования токена."""

    username = serializers.CharField(max_length=MAX_LEN_NAME, required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=data.get('username'))
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Некорректный проверочный код.')
        return data
