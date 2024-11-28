from django.utils.deprecation import MiddlewareMixin
from corsheaders.middleware import CorsMiddleware
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class CustomCorsMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.cors_middleware = CorsMiddleware(get_response)

    def __call__(self, request):
        logger.info(f"Received {request.method} request for {request.path}")
        response = self.cors_middleware(request)
        if request.method == "OPTIONS":
            logger.info("Handling preflight request")
            return self.process_preflight(request)
        return self.process_response(request, response)

    def process_preflight(self, request):
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Max-Age"] = "86400"
        response["Content-Length"] = "0"
        response["Content-Type"] = "text/plain"
        logger.info(f"Preflight response headers: {response}")
        return response

    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken"
        response["Access-Control-Allow-Credentials"] = "true"
        logger.info(f"CORS headers applied for {request.method} {request.path}: {response}")
        return response
