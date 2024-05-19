import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category, Genre, Title, GenreTitle, Review, Comment, User
)

RATIO_DATA = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',

}


# class Command(BaseCommand):
#     help = 'Команда добавляет данные в БД из csv файлов'
#
#     def handle(self, *args, **kwargs):
#         for model, file in RATIO_DATA.items():
#             with open(
#                 f'{settings.BASE_DIR}/static/data/{file}',
#                 'r', encoding='utf-8'
#             ) as csv_data:
#                 reader = csv.DictReader(csv_data)
#                 model.objects.bulk_create(model(**data) for data in reader)
#             self.stdout.write(self.style.SUCCESS('Загрузка прошла успешно'))

class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        for model, base in RATIO_DATA.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Successfully load data'))

