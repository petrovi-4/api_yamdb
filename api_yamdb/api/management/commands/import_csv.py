"""Дополнительные команды проекта"""
import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, GenreTitle, Title, Review, Comment
from user.models import User

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')

FILE_MODEL = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'users.csv': User,
    'review.csv': Review,
    'comments.csv': Comment
}


class Command(BaseCommand):
    """Команда импорта данных из csv файла"""

    def file_path(self, file_name):
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.isfile(file_path):
            return file_path
        raise Exception(f'В директории {DATA_DIR} не найден файл {file_name}')

    def upload_csv(self, file_name, model):
        file_path = self.file_path(file_name)
        try:
            with open(file_path, 'rt', encoding='utf8') as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Данные из файла {file_name} успешно загружены'
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    (
                        f'Возникла ошибка при загрузке данных'
                        f' из файла {file_name}: {error}'
                    )
                )
            )

    def handle(self, *args, **options):
        for file, model in FILE_MODEL.items():
            self.upload_csv(file_name=file, model=model)
