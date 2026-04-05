import logging
import time

from django.shortcuts import render

logger = logging.getLogger("core")


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = time.time()
        response = self.get_response(request)
        duration_ms = int((time.time() - started) * 1000)
        logger.info("%s %s -> %s (%sms)", request.method, request.path, response.status_code, duration_ms)
        return response


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Frame-Options"] = "DENY"
        response["X-Content-Type-Options"] = "nosniff"
        response["Referrer-Policy"] = "same-origin"
        response["Content-Security-Policy"] = "default-src 'self'"
        return response


class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            logger.exception("Unhandled server error while processing %s", request.path)
            return render(request, "core/error.html", status=500)
