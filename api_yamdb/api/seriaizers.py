from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers

from api.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений"""
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        optional_fields = ('description',)
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        # reviews = Review.objects.filter(title=obj)
        # if reviews.exists():
        #     return reviews.aggregate(Avg('score'))
        return 0

    def validate(self, data):
        title_year = int(data['year'])
        current_year = datetime.now().year
        if title_year > current_year:
            raise serializers.ValidationError(
                'Год не может быть больше нынешнего.'
            )
        if Title.objects.filter(name=data['name'], year=data['year']).exists():
            raise serializers.ValidationError(
                'Такой фильм уже есть в базе.'
            )
        return data

    def to_representation(self, obj):
        self.fields['genre'] = GenreSerializer(many=True)
        self.fields['category'] = CategorySerializer()
        return super().to_representation(obj)
