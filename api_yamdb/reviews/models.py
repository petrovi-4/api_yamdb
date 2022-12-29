"""Модели приложения YaMDb"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import max_value_current_year

user = get_user_model()


class Category(models.Model):
    """Модель категории произведений"""

    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        primary_key=True,
        max_length=50,
        verbose_name='Слаг категории'
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведений"""

    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        primary_key=True,
        max_length=50,
        verbose_name='Слаг жанра'
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        db_index=True,
        validators=(max_value_current_year,),
        verbose_name='Год'
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    """Модель для связи жанров и произведений."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        verbose_name='Время добавления', auto_now_add=True
    )

    def __str__(self):
        return f'Оценка {self.author.username} на {self.title.name}'

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_review'
            )
        ]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью',
    )
    pub_date = models.DateTimeField(
        verbose_name='Время добавления', auto_now_add=True
    )

    def __str__(self):
        return f'Оценка {self.author.username} на {self.review.title.name}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
