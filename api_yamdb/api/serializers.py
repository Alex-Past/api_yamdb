from rest_framework import serializers

from reviews.models import Category, Genre, Title, TitleGenre


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайз"""
    class Meta:
        fields = ('name_cat', 'slug_cat')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
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
