"""Сборник абстрактных моделей"""

from django.db import models


class NameSlug(models.Model):
    """Абстрактная модель. Содержит название и Slug."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
