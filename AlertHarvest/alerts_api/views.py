# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from .models import Alert, BlackoutRule

import json
from datetime import datetime
from django.utils import timezone as django_timezone

from alerts_notificator.notifications import send_notification

def is_alert_blackout(alert_data):
    blackout_rules = BlackoutRule.objects.all()

    # Convert the timestamp to an offset-aware datetime
    alert_timestamp_naive = datetime.strptime(alert_data['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
    alert_timestamp_aware = django_timezone.make_aware(alert_timestamp_naive, timezone=django_timezone.get_current_timezone())

    for rule in blackout_rules:
        if (not rule.source or rule.source == alert_data['source']) and \
           (not rule.location or rule.location == alert_data['location']) and \
           (not rule.message_contains_word or rule.message_contains_word in alert_data['message']) and \
           (rule.start_date <= alert_timestamp_aware <= rule.end_date):
            return True

    return False

@csrf_exempt
@require_http_methods(["POST"])
def create_alert(request):
    try:
        data = json.loads(request.body)
        
        alert, created = Alert.objects.get_or_create(
            location=data['location'],
            severity=data['severity'],
            message=data['message'],
            source=data['source'],
            defaults={'timestamp': data['timestamp']}
        )
        alert.last_occurrence = data['timestamp']

        # Check if the existing alert is closed and reopen it
        if alert.status == "CLOSED":
            alert.status = "OPEN"

        #Check if alert falls into blackout period
        alert.blackout = is_alert_blackout(data)
        
        # Save alert properties to DB
        alert.save()
        
        # Send Alert recepit notification
        if settings.NOTIFICATION_ENABLED and not alert.blackout:
            send_notification(alert.id)

        if created:
            # Return success response for a newly created alert
            return JsonResponse({"status": "success", "message": "Alert received and saved."})
        else:
            # Return success response for an existing alert
            return JsonResponse({"status": "success", "message": "Alert already existed. Last Occurrence updated"})
    except Exception as e:
        # Return error response if any exception occurs
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def close_alert(request, alert_id):
    try:
        alert = get_object_or_404(Alert, id=alert_id)
        alert.update_status('CLOSED')
        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alert closed successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def close_alerts_bulk(request):
    try:
        data = json.loads(request.body)
        print(data)
        alert_ids = data.get('alert_ids', None)

        if not alert_ids or not isinstance(alert_ids, list):
            raise ValueError('Invalid or missing "alert_ids" in the request body')

        # Iterate over the list of alert IDs and close each relevant alert
        for alert_id in alert_ids:
            alert = get_object_or_404(Alert, id=alert_id)
            alert.update_status('CLOSED')

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alerts closed successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def close_expired_alerts(request):
    try:
        # Update status to 'CLOSED' for all expired alerts
        updated_count = Alert.objects.filter(status='EXPIRED').update(status='CLOSED')

        if updated_count > 0:
            # Return success response
            return JsonResponse({'status': 'success', 'message': 'Expired alerts closed successfully'})
        else:
            # Return a response indicating that no expired alerts were found
            return JsonResponse({'status': 'success', 'message': 'No expired alerts found'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def acknowledge_alert(request, alert_id):
    try:
        alert = get_object_or_404(Alert, id=alert_id)
        alert.update_status('ACKNOWLEDGED')
        alert.acknowledged_at = datetime.now()

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alert acknowledged successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def acknowledge_alerts_bulk(request):
    try:
        data = json.loads(request.body)
        alert_ids = data.get('alert_ids', None)

        if not alert_ids or not isinstance(alert_ids, list):
            raise ValueError('Invalid or missing "alert_ids" in the request body')

        # Iterate over the list of alert IDs and acknowledge each relevant alert
        for alert_id in alert_ids:
            alert = get_object_or_404(Alert, id=alert_id)
            alert.update_status('ACKNOWLEDGED')
            alert.acknowledged_at = datetime.now()

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alerts acknowledged successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def unacknowledge_alert(request, alert_id):
    try:
        alert = get_object_or_404(Alert, id=alert_id)
        alert.update_status('OPEN')
        alert.acknowledged_at = None

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alert unacknowledged successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def pin_alert(request, alert_id):
    try:
        alert = get_object_or_404(Alert, id=alert_id)
        alert.pinned = True
        alert.save()

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alert pinned successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["PUT"])
def unpin_alert(request, alert_id):
    try:
        alert = get_object_or_404(Alert, id=alert_id)
        alert.pinned = False
        alert.save()

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alert unpinned successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)