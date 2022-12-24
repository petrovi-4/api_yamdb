from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import get_jwt, send_code, UserViewSet, UserAdminViewSet

app_name = "user"

router = DefaultRouter()
router.register("users", UserAdminViewSet, basename="users")

urlpatterns = [
    path("auth/sigup/", send_code),
    path("auth/token/", get_jwt),
    path("users/me/", UserViewSet),
    path("", include(router.urls)),
]
