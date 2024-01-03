from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("dashboard/", views.alerts_dashboard, name="alerts_dashboard"),
    path("analytics/", views.alerts_analytics, name="alerts_analytics"),
    path('display/<int:pk>/', views.alert_details, name = "alert_details"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='/viz/login/'), name="logout")
]