import logging
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication

# restrict message access time
from django.http import HttpResponseForbidden

#offensivelanguagemiddleware
import time
from django.http import JsonResponse
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    """Logs in the user, user request and time of the request."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()
    
    def __call__(self, request):
        user = "Anonymous"
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header and auth_header.startswith('Bearer'):
            try:
                validated_user = self.jwt_authenticator.authenticate(request)
                if validated_user:
                    user = validated_user[0].username
            except Exception as e:
                print("JWT authentication failed", str(e))
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """allow the users only to access their messages within a certain time window."""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        now = datetime.now().now()

        if not (now.hour >= 3 and now.hour <=21):
            return HttpResponseForbidden("Access to the messaging app is restricted to 1800hrs - 2100hrs ")        
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """checks the number of messages sent from a given IP address and restricts to only 3 messages per minute."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list) #{ip: [timestamp,...]}
        self.lock = Lock()
        self.max_messages = 1
        self.time_window = 60 # seconds


    def __call__(self, request):
        if request.path.startswith("/api/chats/") and request.method == 'POST':
            ip = self.get_ip(request)
            now = time.time()

            with self.lock:
                timestamps = self.message_log[ip]
                timestamps = [ts for ts in timestamps if now - ts < self.time_window] # remove older timestamps
                if len(timestamps) >=self.max_messages:
                    return JsonResponse({
                        "error": "Rate limit exceeded. Maximun of 1 message per minute"
                    }, status = 429)
                timestamps.append(now)
                self.message_log[ip] = timestamps
            print(timestamps)
        return self.get_response(request)
    
    def get_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        user = None
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)

        if auth_header and auth_header.startswith("Bearer"):
            try:
                validated = self.jwt_authenticator.authenticate(request)
                if validated:
                    user = validated[0]
                    print("I am ", user.username)
            except Exception as e:
                return JsonResponse({"detail": "Forbidden"}, status=403)
            
        if user:
            if not (user.is_staff or user.is_superuser):
                return JsonResponse({"detail": "Forbidden"}, status = 403)
        return self.get_response(request)


