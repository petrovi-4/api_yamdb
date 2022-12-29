from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import get_jwt, send_code, UserViewSet

app_name = "user"

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/signup/", send_code),
    path("auth/token/", get_jwt),
    path("", include(router.urls)),
]
