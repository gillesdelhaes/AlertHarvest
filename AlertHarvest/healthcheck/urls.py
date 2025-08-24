from django.urls import path
from .views import healthcheck

urlpatterns = [
    path("", healthcheck, name="healthcheck"),
]