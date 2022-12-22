from django.urls import path, include
from rest_framework.routers import DefaultRouter

from access.views import get_jwt, send_code, UsersViewSet, UserAdminViewSet

app_name = "access"

router = DefaultRouter()
router.register("users", UserAdminViewSet, basename="users")

urlpatterns = [
    path("auth/sigup/", send_code),
    path("auth/token/", get_jwt),
    path("users/me/", UsersViewSet.as_view()),
    path("", include(router.urls)),
]
