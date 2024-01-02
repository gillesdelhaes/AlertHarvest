from alerts_api.models import Alert

def send_notification(alert):
    notification_info = f"SLACK - Received alert notification"
    with open('notification_log.txt', 'a') as file:
        file.write(notification_info + '\n')