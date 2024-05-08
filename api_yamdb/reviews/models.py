from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name_cat = models.TextField(
        verbose_name='Наименование категории', max_length=256
    )
    slug_cat = models.SlugField(
        unique=True, verbose_name='Слаг категории', max_length=256
    )


class Genre(models.Model):
    name_genre = models.TextField(
        verbose_name='Наименование жанра', max_length=256
    )
    slug_genre = models.SlugField(
        unique=True, verbose_name='Слаг жанра', max_length=50
    )


class Title(models.Model):
    name = models.TextField(verbose_name='Название', max_length=256)
    year = models.DateTimeField(verbose_name='Год выпуска')
    # Рейтинг мне кажется надо рассчитывать в сериализаторе. Как думаете?
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Категория')


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True,
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


# class Review(models.Model):
#     title = models.ForeignKey(
#         Title, on_delete=models.CASCADE, verbose_name='Произведение'
#     )
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name='Автор отзыва'
#     )
#     text = models.TextField(verbose_name='Текст отзыва')
#     # Не знаю, какой тип поля лучше выбрать в score
#     score = models.PositiveSmallIntegerField(verbose_name='Оценка')
#     pub_date = models.DateTimeField(
#         verbose_name='Дата отзыва', auto_now_add=True
#     )
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
