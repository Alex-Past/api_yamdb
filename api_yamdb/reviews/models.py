from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from consts import MAX_LEN_NAME, LENGTH_TEXT

User = get_user_model()


class Category(models.Model):
    """Модель для категорий (типов) произведений."""

    name = models.TextField(
        verbose_name='Наименование категории', max_length=MAX_LEN_NAME
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Genre(models.Model):
    """Модель для жанров произведений."""

    name = models.TextField(
        verbose_name='Наименование жанра', max_length=MAX_LEN_NAME
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


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
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )
    description = models.TextField(
        verbose_name='Описание', blank=True
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class GenreTitle(models.Model):
    """Промежуточная модель для произведений и жанров."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f'{self.genre} {self.title}'[:LENGTH_TEXT]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Класс комментариев."""

    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='oтзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LENGTH_TEXT]
