from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models.functions import TruncDate
from alerts_api.models import Alert
from datetime import datetime, timedelta

def update_expired_status():
    now = datetime.now()
    expiration_time = now - timedelta(hours=36)

    # Update status to 'EXPIRED' where last_occurrence is less than or equal to expiration_time
    Alert.objects.filter(Q(last_occurrence__lte=expiration_time) & (Q(status='OPEN') | Q(status='ACKNOWLEDGED'))).update(status='EXPIRED')

    # Update status to 'OPEN' where last_occurrence is greater than expiration_time and status is 'EXPIRED'
    Alert.objects.filter(last_occurrence__gt=expiration_time, status='EXPIRED').update(status='OPEN')

# Create your views here.

def alerts_dashboard(request):
    #Refresh expired flag for all alerts
    update_expired_status()
    
    #All Alerts not closed
    alerts = Alert.objects.exclude(status="CLOSED").order_by('status', 'last_occurrence', 'location', 'severity', 'source', 'message')
    sorted_alerts = sorted(alerts, key=lambda x: (
        x.status != 'OPEN',  # Put 'OPEN' status first
        x.status != 'ACKNOWLEDGED',  # Then 'ACKNOWLEDGED'
        x.status != 'EXPIRED',  # Then 'EXPIRED'
        x.severity != 'CRITICAL',  # Then 'CRITICAL' severity
        x.severity != 'MAJOR',  # Then 'MAJOR' severity
        x.severity != 'WARNING',  # Then 'WARNING' severity
        x.last_occurrence,  # Finally, sort by last_occurrence
    ))  
    
    critical_open_count = Alert.objects.filter(severity="CRITICAL", status="OPEN").count()
    major_open_count = Alert.objects.filter(severity="MAJOR", status="OPEN").count()
    warning_open_count = Alert.objects.filter(severity="WARNING", status="OPEN").count()
    acknowledged_count = Alert.objects.filter(status="ACKNOWLEDGED").count()
    expired_count = Alert.objects.filter(status="EXPIRED").count()
    
     # Calculate the date 30 days ago from today
    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Count new tickets created per day for the past 30 days
    new_tickets_per_day = (
        Alert.objects.filter(timestamp__gte=thirty_days_ago)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(new_tickets_count=Count('id'))
        .order_by('date')
    )

    # Extract counts and dates for chart data
    thirtyday_chart_labels = [entry['date'] for entry in new_tickets_per_day]
    thirtyday_chart_labels_formatted = [date_obj.strftime('%Y-%m-%d') for date_obj in thirtyday_chart_labels]
    thirtyday_chart_data = [entry['new_tickets_count'] for entry in new_tickets_per_day]
    
    #Created context dict
    context = { 'alerts': sorted_alerts,
                'critical_count': critical_open_count,
                'major_count': major_open_count,
                'warning_count': warning_open_count,
                'acknowledged_count': acknowledged_count,
                'expired_count': expired_count,
                'thirtyday_chart_labels': thirtyday_chart_labels_formatted,
                'thirtyday_chart_data':thirtyday_chart_data
                }
    return render(request, 'alerts_visualization/dashboard.html', context)

def alerts_analytics(request):
    #Refresh expired flag for all alerts
    update_expired_status()
    #### 30 Days Chart Section #####
    # Calculate the date 30 days ago from today
    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Count new tickets created per day for the past 30 days
    new_tickets_per_day = (
        Alert.objects.filter(timestamp__gte=thirty_days_ago)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(new_tickets_count=Count('id'))
        .order_by('date')
    )

    # Extract counts and dates for chart data
    thirtyday_chart_labels = [entry['date'] for entry in new_tickets_per_day]
    thirtyday_chart_labels_formatted = [date_obj.strftime('%Y-%m-%d') for date_obj in thirtyday_chart_labels]
    thirtyday_chart_data = [entry['new_tickets_count'] for entry in new_tickets_per_day]
    
    #### Severity doughnut chart section ####
    # Count open alerts per severity
    open_alerts_by_severity = (
        Alert.objects.filter(status='OPEN')
        .values('severity')
        .annotate(open_alerts_count=Count('id'))
        .order_by('severity')
    )

    # Extract counts and severity labels for doughnut chart data
    severity_chart_labels = [entry['severity'] for entry in open_alerts_by_severity]
    severity_chart_data = [entry['open_alerts_count'] for entry in open_alerts_by_severity]

    
    ### Source doughnut section ###
    # Count new alerts per source for the past 30 days
    alerts_by_source = (
        Alert.objects.filter(timestamp__gte=thirty_days_ago)
        .values('source')
        .annotate(alerts_count=Count('id'))
        .order_by('-alerts_count')  # Order by count in descending order
    )

    # Extract counts and source labels for doughnut chart data
    source_chart_labels = [entry['source'] for entry in alerts_by_source]
    source_chart_data = [entry['alerts_count'] for entry in alerts_by_source]


    ### Location bar section ####
    # Count alarms per location for the past 30 days
    alarms_by_location = (
        Alert.objects.filter(timestamp__gte=thirty_days_ago)
        .values('location')
        .annotate(alarms_count=Count('id'))
        .order_by('alarms_count')  # Order by count in ascending order
    )

    # Extract counts and location labels for horizontal bar chart data
    location_chart_labels = [entry['location'] for entry in alarms_by_location]
    location_chart_data = [entry['alarms_count'] for entry in alarms_by_location]

    # Created context dict
    context = {
        'thirtyday_chart_labels': thirtyday_chart_labels_formatted,
        'thirtyday_chart_data': thirtyday_chart_data,
        'severity_chart_labels': severity_chart_labels,
        'severity_chart_data': severity_chart_data,
        'source_chart_labels': source_chart_labels,
        'source_chart_data': source_chart_data,
        'location_chart_labels': location_chart_labels,
        'location_chart_data': location_chart_data,
    }
    
    return render(request, 'alerts_visualization/analytics.html', context)

def alert_details(request, pk):
    #Refresh expired flag for all alerts
    update_expired_status()
    # Fetch the Alert object based on the primary key (pk)
    alert = get_object_or_404(Alert, pk=pk)

    # Pass the alert object to the template context
    context = {'alert': alert}

    # Render the template with the context
    return render(request, 'alerts_visualization/alert_details.html', context)