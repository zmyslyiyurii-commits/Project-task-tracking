import time
from django.utils import timezone
from .models import UserActivity

class ActivityTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = time.time()

            if last_activity:
                duration = now - last_activity
                # Якщо пауза між кліками менше 5 хв (300с), враховуємо це як активне користування
                if duration < 300:
                    today = timezone.now().date()
                    activity, created = UserActivity.objects.get_or_create(
                        user=request.user, 
                        date=today
                    )
                    activity.seconds_spent += int(duration)
                    activity.save()

            request.session['last_activity'] = now

        response = self.get_response(request)
        return response