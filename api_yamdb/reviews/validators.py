from django.utils import timezone
from django.core.exceptions import ValidationError


def max_value_current_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError('Год не может быть больше нынешнего.')
    return value

