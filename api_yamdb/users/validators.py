import re

from django.core.exceptions import ValidationError


def username_validator(value):
    """Кастомный валидатор имени пользователя."""
    regex = r'^[\w.@+-]+\Z'
    invalid_values = re.sub(regex, ', ', value)
    if value in invalid_values:
        raise ValidationError(
            f'Недопустимые символы: {invalid_values}'
        )
    elif value == 'me':
        raise ValidationError('Нельзя использовать имя "me".')
    return value
