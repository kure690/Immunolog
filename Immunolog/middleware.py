from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            user_sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_data__contains=str(request.user.id)
            ).exclude(session_key=current_session_key)
            
            # Delete other sessions
            for session in user_sessions:
                session.delete()

        response = self.get_response(request)
        return response

class ClearMessagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear messages at the beginning of each request
        storage = messages.get_messages(request)
        storage.used = True

        response = self.get_response(request)
        return response