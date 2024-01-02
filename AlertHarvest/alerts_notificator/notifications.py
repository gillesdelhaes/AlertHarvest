from .tasks import process_alert_notification

def send_notification(alert_id):
    # Trigger Celery task to handle notification asynchronously
    process_alert_notification.delay(alert_id)
