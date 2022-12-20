from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    title = models.ForeignKey(
        # to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        # to=
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.SmallIntegerField(
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
        verbose_name = ('Обзор',)
        verbose_name_plural = 'Обзоры'

        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_review'
            )
        ]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текс')
    author = models.ForeignKey(
        # to=
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
