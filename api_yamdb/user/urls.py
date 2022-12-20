from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegistrationAPIView, SendCodeAPIView

app_name = 'user'

router_v1 = DefaultRouter()
router_v1.register("registration", SendCodeAPIView, basename="posts")
router_v1.register("token", RegistrationAPIView, basename="token")

urlpatterns = [
    path('auth/', include(router_v1.urls)),
]
