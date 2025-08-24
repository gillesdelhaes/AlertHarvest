from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("dashboard/", views.alerts_dashboard, name="alerts_dashboard"),
    path("analytics/", views.alerts_analytics, name="alerts_analytics"),
    path('display/<int:pk>/', views.alert_details, name = "alert_details"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='/viz/login/'), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html",
        success_url="/viz/password_change/done/"
    ), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"
    ), name="password_change_done"),
    path('autosave_notes/', views.auto_save_notes, name='auto_save_notes'),
    path('blackout_rules/', views.blackout_rules, name='blackout_rules'),
    path('create_blackout_rule/', views.create_blackout_rule, name='create_blackout_rule'),
    path('system-health/', views.system_health, name='system_health'),
]