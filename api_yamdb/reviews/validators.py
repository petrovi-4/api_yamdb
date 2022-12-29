"""Валидаторы для моделей reviews"""
from django.core.exceptions import ValidationError
from django.utils import timezone


def max_value_current_year(value):
    """Валидатор года."""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError('Год не может быть больше нынешнего.')
    return value
