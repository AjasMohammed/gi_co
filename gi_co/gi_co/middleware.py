from django.core.cache import cache
from django.http import JsonResponse


REQUEST_LIMIT = 100 # per 5 minutes.

class TrafficHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timeout = 5*60
        ip_address = request.META.get("REMOTE_ADDR")
        ip_data = cache.get(ip_address, 0)
        print(f"{ip_address}: count={ip_data}")
        if ip_data == 0:
            cache.set(ip_address, 1, timeout)
        elif ip_data >= REQUEST_LIMIT:
            return JsonResponse({"error": "Too many requests, try again after sometime!", "status_code": 429}, status=429)
        else:
            cache.incr(ip_address)
        response = self.get_response(request)

        return response