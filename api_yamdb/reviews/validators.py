from django.utils import timezone


def validate_year(year):
    if year > timezone.now().year:
        raise ValueError(f'Некорректный год произведения')
