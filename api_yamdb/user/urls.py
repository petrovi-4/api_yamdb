from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import get_jwt, send_code, UsersViewSet, UserAdminViewSet

app_name = "user"

router = DefaultRouter()
router.register("users", UserAdminViewSet, basename="users")

urlpatterns = [
    path("v1/auth/sigup/", send_code),
    path("v1/auth/token/", get_jwt),
    path("v1/users/me/", UsersViewSet.as_view()),
    path("", include(router.urls)),
]
