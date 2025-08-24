from django.http import JsonResponse
from .utils import get_system_health

def healthcheck(request):
    """
    Returns JSON with each component's status AND overall health.
    """
    data = get_system_health()

    # Overall is True only if all components are 'OK'
    overall = all(v == 'OK' for v in data.values())

    return JsonResponse(
        {
            "status": data,      # detailed per-service info
            "healthy": overall   # overall boolean
        },
        status=200 if overall else 503
    )
