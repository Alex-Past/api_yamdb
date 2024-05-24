from django.contrib.auth.models import AbstractUser
from django.db import models

from . import validators


MAX_LEN_NAME = 150

MAX_LEN_EMAIL = 254


class User(AbstractUser):

    class UserRole(models.TextChoices):

        USER = 'user', 'Пользователь',
        MODERATOR = 'moderator', 'Модератор',
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LEN_NAME,
        unique=True,
        validators=[validators.username_validator],
    )
    first_name = models.CharField(max_length=MAX_LEN_NAME, blank=True)
    last_name = models.CharField(max_length=MAX_LEN_NAME, blank=True)
    email = models.EmailField('Email', max_length=MAX_LEN_EMAIL, unique=True)
    role = models.CharField(
        'Роль пользователя',
        choices=UserRole.choices,
        max_length=max(len(role[1]) for role in UserRole.choices),
        default=UserRole.USER
    )
    bio = models.TextField('Биография', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return (self.role == self.UserRole.ADMIN
                or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR
