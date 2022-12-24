"""Модели приложения YaMDb"""
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

user = get_user_model()


class Comment(models.Model):
    text = models.TextField(verbose_name="Текс")
    author = models.ForeignKey(
        to=user,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Ревью",
    )
    pub_date = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)

    def __str__(self):
        return f"Оценка {self.author.username} на {self.review.title.name}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Category(models.Model):
    """Модель категории произведений"""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведений"""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.CharField(max_length=1800, blank=True)
    genre = models.ManyToManyField(Genre, through="GenreTitle", related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="titles", null=True
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи жанров и произведений."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]
        verbose_name = "Связь"
        verbose_name_plural = "Связи"

    def __str__(self):
        return f"{self.genre} {self.title}"


class Review(models.Model):
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        to=user,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)

    def __str__(self):
        return f"Оценка {self.author.username} на {self.title.name}"

    class Meta:
        verbose_name = ("Обзор",)
        verbose_name_plural = "Обзоры"

        constraints = [
            models.UniqueConstraint(fields=("title", "author"), name="unique_review")
        ]
