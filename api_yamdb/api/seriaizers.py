from datetime import datetime

from review.models import Category, Genre, Title, Comment, Review

from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


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
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        optional_fields = ('description',)
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        if reviews.exists():
            query = reviews.aggregate(average_score=Avg('score'))
            return round(query['average_score'])
        return None

    def validate(self, data):
        request = self.context.get('request')
        title_year = int(data['year'])
        current_year = datetime.now().year
        if title_year > current_year:
            raise serializers.ValidationError(
                'Год не может быть больше нынешнего.'
            )
        if (
            request.method == 'POST'
            and Title.objects.filter(
                name=data['name'], year=data['year']
            ).exists()
        ):
            raise serializers.ValidationError('Такой фильм уже есть в базе.')
        return data

    def to_representation(self, obj):
        self.fields['genre'] = GenreSerializer(many=True)
        self.fields['category'] = CategorySerializer()
        return super().to_representation(obj)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставили свой отзыв к этому призведению!'
            )
        return data

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review
