from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from reviews.consts import LENGTH_TEXT, MAX_LEN_NAME, SCORE_VALIDATOR
from reviews.validators import validate_year

User = get_user_model()


class BaseModel(models.Model):
    """Базовая модель для категорий и жанров произведения."""

    name = models.CharField(
        verbose_name='Наименование', max_length=MAX_LEN_NAME
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг', db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Category(BaseModel):
    """Модель для категорий (типов) произведений."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(BaseModel):
    """Модель для жанров произведений."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    """Модель для произведения."""

    name = models.CharField(verbose_name='Название', max_length=MAX_LEN_NAME)
    year = models.SmallIntegerField(
        verbose_name='Год выпуска', validators=[validate_year], db_index=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр', db_index=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория', db_index=True
    )
    description = models.TextField(
        verbose_name='Описание', blank=True
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class GenreTitle(models.Model):
    """Промежуточная модель для произведений и жанров."""

    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'[:LENGTH_TEXT]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=SCORE_VALIDATOR,
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
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:LENGTH_TEXT]


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
