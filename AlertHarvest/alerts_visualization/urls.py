from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.alerts_dashboard, name="alerts_dashboard"),
    path("analytics/", views.alerts_analytics, name="alerts_analytics"),
    path('display/<int:pk>/', views.alert_details, name = "alert_details"),
]