from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.conf import settings

import redis
from celery import current_app as celery_app


def healthcheck(request):
    status = {
        "django": True,
        "database": False,
        "redis": False,
        "celery": False,
    }

    # Database check (SQLite in your case)
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT 1;")
        status["database"] = True
    except OperationalError:
        pass

    # Redis check
    try:
        r = redis.Redis.from_url(settings.CELERY_BROKER_URL)
        status["redis"] = r.ping()
    except Exception:
        pass

    # Celery check
    try:
        if celery_app.control.ping(timeout=1.0):
            status["celery"] = True
    except Exception:
        pass

    overall = all(status.values())
    return JsonResponse(
        {"status": status, "healthy": overall},
        status=200 if overall else 503
    )
