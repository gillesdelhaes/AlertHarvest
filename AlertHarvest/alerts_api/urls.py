from django.urls import path

from . import views

urlpatterns = [
    path('create_alert/', views.create_alert, name='create_alert'),
    path('delete_alert/', views.delete_alert, name='delete_alert'),
    path('delete_expired_alerts/', views.delete_expired_alerts, name='delete_expired_alerts'),
    path('close_alert/', views.close_alert, name='close_alert'),
    path('close_alerts_bulk/', views.close_alerts_bulk, name='close_alerts_bulk'),
    path('close_expired_alerts/', views.close_expired_alerts, name='close_expired_alerts'),
    path('acknowledge_alert/', views.acknowledge_alert, name='acknowledge_alert'),
    path('acknowledge_alerts_bulk/', views.acknowledge_alerts_bulk, name='acknowledge_alerts_bulk'),
    path('unacknowledge_alert/', views.unacknowledge_alert, name='unacknowledge_alert'),
]