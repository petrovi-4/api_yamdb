from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc',
    ),
    path('api/', include('api.urls'), name='api'),
    path('api/v1/', include('user.urls'), name='user'),
]
