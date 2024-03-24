from .models import User
from django.utils import timezone
from datetime import timedelta


class NoneActiveDeleterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_limit = timezone.now() - timedelta(minutes=5)
        for user in User.objects.filter(is_active=False, otp_created_at__lt=time_limit):
            user.delete()

        response = self.get_response(request)

        return response
