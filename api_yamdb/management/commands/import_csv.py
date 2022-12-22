"""Дополнительные команды проекта"""
from django.core.management.base import BaseCommand, CommandError

from api_yamdb.models import Category, Genre, Title

class Command(BaseCommand):
    """Команда импорта данных из csv файла"""

    def handle(self, *args, **options):
        pass
