"""View приложения YaMDb"""

from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from api_yamdb.models import Category, Genre, Title
from api_yamdb.permissions import CustomAdminPermission
from api_yamdb.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)


class CategoryViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    """Вьюсет категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (CustomAdminPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    """Вьюсет жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (CustomAdminPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет постов"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #permission_classes = (CustomAdminPermission,)
    pagination_class = PageNumberPagination
