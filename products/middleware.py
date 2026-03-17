import time

class CacheDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Process request → view
        response = self.get_response(request)

        # Calculate time (ms)
        duration = (time.time() - start_time) * 1000

        # Add headers
        response["X-Cache-Time"] = f"{duration:.2f}ms"

        # Optional: attach cache key if view sets it
        cache_key = getattr(request, "cache_key", None)
        if cache_key:
            response["X-Cache-Key"] = cache_key

        return response