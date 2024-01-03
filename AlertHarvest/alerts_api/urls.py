from django.urls import path
from . import views

urlpatterns = [
    path('create_alert/', views.create_alert, name='create_alert'),
    path('close_alert/<int:alert_id>/', views.close_alert, name='close_alert'),
    path('close_alerts_bulk/', views.close_alerts_bulk, name='close_alerts_bulk'),
    path('close_expired_alerts/', views.close_expired_alerts, name='close_expired_alerts'),
    path('acknowledge_alert/<int:alert_id>/', views.acknowledge_alert, name='acknowledge_alert'),
    path('acknowledge_alerts_bulk/', views.acknowledge_alerts_bulk, name='acknowledge_alerts_bulk'),
    path('unacknowledge_alert/<int:alert_id>/', views.unacknowledge_alert, name='unacknowledge_alert'),
]