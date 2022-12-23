"""Дополнительные команды проекта"""
import csv
import os

from django.shortcuts import get_object_or_404

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from api.models import Category, Genre, GenreTitle, Title

# file_name = os.path.basename(file)
# file_path = os.path.realpath(file)

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')

FILE_MODEL = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle
}


class Command(BaseCommand):
    """Команда импорта данных из csv файла"""

    def list_csv(self):
        file_list = []
        for f in os.listdir(DATA_DIR):
            if f.endswith('.csv'):
                # print(os.path.realpath(f))
                print(os.path.abspath(f))
                # file_list.append(f)
        return file_list

    # def fill_model(self, path):
    #     with open(path, 'rt') as f:
    #         reader = csv.reader(f, dialect='excel')
    #         for row in reader:
    #             Question.objects.create(
    #                 attr1=row[0],
    #                 attr2=row[1],
    #             )

    def file_path(self, file_name):
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.isfile(file_path):
            return file_path
        raise Exception(f'В директории {DATA_DIR} не найден файл {file_name}')

    def model_fields(self, model):
        fields_dict = {}
        for field in model._meta.get_fields():
            fields_dict[field.name] = type(field).__name__
        # fields_list = [f.name for f in model._meta.get_fields()]
        return fields_dict

    # def fill_model(self, filename):
    #     category_path = self.file_path('category.csv')
    #     try:
    #         with open(category_path, 'rt', encoding='utf8') as f:
    #             reader = csv.reader(f, dialect='excel')
    #             next(reader)
    #             for row in reader:
    #                 table_record = 0
    #                 category = Category.objects.create(
    #                     id=row[0],
    #                     name=row[1],
    #                     slug=row[2]
    #                 )
    #             # category.save()
    #     except Exception as error:
    #         print(error)

    def upload_csv(self, file_name, model):
        file_path = self.file_path(file_name)
        try:
            with open(file_path, 'rt', encoding='utf8') as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Данные модели {model} успешно загружены'
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    (f'Возникла ошибка при загрузке данных'
                     f' в модель {model}: {error}')
                )
            )
    def upload_titles(self):
        file_path = self.file_path('titles.csv')
        try:
            with open(file_path, 'rt', encoding='utf8') as csv_file:
                titles_batch = []
                reader = csv.DictReader(csv_file)
                next(reader)
                for row in reader:
                    title_object = Title(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category_id=row[3]
                    )
                    titles_batch.append(title_object)
                Title.objects.bulk_create(titles_batch)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Данные модели {Title.name} успешно загружены'
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    (f'Возникла ошибка при загрузке данных'
                     f' в модель {Title.name}: {error}')
                )
            )


    def handle(self, *args, **options):
        # self.upload_csv(file_name='category.csv', model=Category)
        # self.upload_csv(file_name='genre.csv', model=Genre)
        # self.upload_csv(file_name='titles.csv', model=Title)
        self.upload_titles()
        # print(self.model_fields(Title))




