from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, TitleGenre, Comment, Review
from consts import MAX_LEN_NAME, MAX_LEN_SLUG
from reviews.models import Category, Genre, Title, TitleGenre


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайз"""
    name_cat = serializers.CharField(
        max_length=MAX_LEN_NAME,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    slug_cat = serializers.SlugField(
        max_length=MAX_LEN_SLUG,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name_cat', 'slug_cat')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name_genre = serializers.CharField(
        max_length=MAX_LEN_NAME,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )
    slug_genre = serializers.SlugField(
        max_length=MAX_LEN_SLUG,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name_genre', 'slug_genre')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(
        many=True,
        # required=False
    )
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genres',
                  'category')

    def create(self, validated_data):
        # По идее проверка не нужна, ведь поле обязательно, но пока оставлю
        if 'genres' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genres')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    **genre)
                TitleGenre.objects.create(
                    genre=current_genre, title=title)
            return title


class CommentSerializer(serializers.ModelSerializer):
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