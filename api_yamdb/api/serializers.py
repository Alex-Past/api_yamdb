from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import DEFAULT_FROM_EMAIL
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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о произведении."""

    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True,
        allow_null=False, allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментарии."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывы."""

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале.')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
                request.method == 'POST'
                and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
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
        max_length=150,
        required=True
    )
    email = serializers.EmailField(max_length=254, required=True)

    def create(self, validated_data):
        try:
            user, create = User.objects.get_or_create(**validated_data)
            username = validated_data.get('username')
            email = validated_data.get('email')
            confirmation_code = default_token_generator.make_token(user)
            send_mail(subject='Регистрация на сайте api_yamdb',
                      message=f'Проверочный код: {confirmation_code}',
                      from_email=DEFAULT_FROM_EMAIL,
                      recipient_list=[email],
                      fail_silently=True, )

        except IntegrityError:
            username = validated_data.get('username')
            email = validated_data.get('email')
            f'Пользователь с именем "{username}" '
            f'и почтой "{email}" уже существует!'
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для использования токена."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)
