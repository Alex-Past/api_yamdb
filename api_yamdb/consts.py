from django.core.validators import MaxValueValidator, MinValueValidator
"""Константы для проекта"""

MAX_LEN_NAME = 256
MAX_LEN_SLUG = 50
LENGTH_TEXT = 15
LENGTH_TEXT = 15

SCORE_VALIDATOR = (MinValueValidator(1), MaxValueValidator(10))
