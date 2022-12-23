"""Дополнительные команды проекта"""
import os
import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.models import Category, Genre, Title, GenreTitle


class Command(BaseCommand):
    """Команда импорта данных из csv файла"""

    def list_files(self):
        data_dir = os.path.join(settings.BASE_DIR, 'static/data')
        file_list = []
        for f in os.listdir(data_dir):
            if f.endswith('.csv'):
                file_list.append(f)
        return file_list

    def handle(self, *args, **options):
        print(self.list_files())
