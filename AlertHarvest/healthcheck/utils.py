# healthcheck/utils.py
import redis
from django.db import connections
from django.conf import settings
from celery import current_app as celery_app

def get_system_health():
    status = {}

    # Check Django itself
    status['django'] = 'OK'

    # Check SQLite
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT 1;")
        status['sqlite'] = 'OK'
    except Exception as e:
        status['sqlite'] = f"ERROR: {e}"

    # Check Redis
    try:
        r = redis.Redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        status['redis'] = 'OK'
    except Exception as e:
        status['redis'] = f"ERROR: {e}"

    # Check Celery
    try:
        if celery_app.control.ping(timeout=1.0):
            status['celery'] = 'OK'
        else:
            status['celery'] = 'No workers responding'
    except Exception as e:
        status['celery'] = f"ERROR: {e}"

    return status
