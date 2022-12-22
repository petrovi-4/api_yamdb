"""YaMDb URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
