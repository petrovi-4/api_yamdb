from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLES = (
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь"),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Ник пользователя",
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Недопустимые символы в имени пользователя",
            )
        ],
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="Адрес электронной почты",
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="Имя пользователя"
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name="Фамилия пользователя"
    )
    bio = models.CharField(
        max_length=100, verbose_name="Биография", blank=True
    )
    role = models.CharField(
        max_length=100, verbose_name="Роль", choices=ROLES, default=USER
    )
    confirmation_code = models.CharField(max_length=6, default="000000")
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
