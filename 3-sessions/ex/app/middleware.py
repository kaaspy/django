import random
from django.conf import settings

def session_handler(request):
    user = request.user
    if user.is_authenticated:
        request.session["username"] = user.username
    else:
        if not request.session.session_key:
            request.session.create()
            request.session["username"] = random.choice(getattr(settings, "ANON_USER_NAMES"))
            request.session.set_expiry(42)

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        session_handler(request)
        response = self.get_response(request)
        return response