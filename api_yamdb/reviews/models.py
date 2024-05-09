from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone

from consts import MAX_LEN_NAME, MAX_LEN_SLUG

User = get_user_model()


class Category(models.Model):
    """Модель для категорий (типов) произведений."""

    name_cat = models.TextField(
        verbose_name='Наименование категории', max_length=MAX_LEN_NAME
    )
    slug_cat = models.SlugField(unique=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name_cat


class Genre(models.Model):
    """Модель для жанров произведений."""

    name_genre = models.TextField(
        verbose_name='Наименование жанра', max_length=MAX_LEN_NAME
    )
    slug_genre = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name_genre


class Title(models.Model):
    """Модель для произведения."""

    name = models.TextField(verbose_name='Название', max_length=MAX_LEN_NAME)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(
                int(timezone.now().year),
                message='Год выпуска не может быть больше текущего'
            )
        ],
    )
    description = models.TextField(
        verbose_name='Описание', blank=True
    )
    genres = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Промежуточная модель для произведений и жанров."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True,
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение', related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор отзыва'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва', auto_now_add=True
    )
#
#
# class Comment(models.Model):
#     review = models.ForeignKey(
#         Review, on_delete=models.CASCADE, verbose_name='Отзыв'
#     )
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name='Автор комментария'
#     )
#     text = models.TextField(verbose_name='Текст комментария')
#     pub_date = models.DateTimeField(
#         verbose_name='Дата комментария', auto_now_add=True
#     )
