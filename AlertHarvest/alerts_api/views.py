# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Alert
import json
from datetime import datetime

from django.conf import settings
from alerts_notificator.notifications import send_notification

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

        # Save alert properties to DB
        alert.save()
        
        # Send Alert recepit notification
        if settings.NOTIFICATION_ENABLED:
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
@require_http_methods(["DELETE"])
def delete_alert(request):
    #alert_id = request.POST.get('alert_id', None)
    try:
        data = json.loads(request.body)
        alert_id = data.get('alert_id', None)
        alert = Alert.objects.get(id=alert_id)
        alert.delete()
        return JsonResponse({'status': 'success', 'message': 'Alert deleted successfully'})
    except Alert.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Alert not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_expired_alerts(request):
    try:
        # Perform the operation to delete expired alerts
        deleted_count, _ = Alert.objects.filter(expired=True).delete()

        if deleted_count > 0:
            # Return success response
            return JsonResponse({'status': 'success', 'message': 'Expired alerts deleted successfully'})
        else:
            # Return a response indicating that no expired alerts were found
            return JsonResponse({'status': 'success', 'message': 'No expired alerts found'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def close_alert(request):
    # alert_id = request.PUT.get('alert_id', None)
    try:
        data = json.loads(request.body)
        alert_id = data.get('alert_id', None)
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
def acknowledge_alert(request):
    # alert_id = request.PUT.get('alert_id', None)

    try:
        data = json.loads(request.body)
        alert_id = data.get('alert_id', None)
        
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
def unacknowledge_alert(request):
    # alert_id = request.PUT.get('alert_id', None)

    try:
        data = json.loads(request.body)
        alert_id = data.get('alert_id', None)
        alert = get_object_or_404(Alert, id=alert_id)
        alert.update_status('OPEN')
        alert.acknowledged_at = None

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Alert unacknowledged successfully'})
    except Exception as e:
        # Return an error response with details
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
