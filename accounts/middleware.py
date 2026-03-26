from django.shortcuts import redirect
from django.urls import reverse

from .models import TeacherProfile


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and self._should_enforce(request.path):
            profile, _ = TeacherProfile.objects.get_or_create(
                teacher=user,
                defaults={
                    'full_name': f'{user.first_name} {user.last_name}'.strip(),
                    'mobile_no': (user.phone or '').strip(),
                },
            )
            if not profile.is_complete:
                return redirect(reverse('accounts:profile'))

        return self.get_response(request)

    def _should_enforce(self, path):
        excluded_prefixes = (
            '/accounts/profile/',
            '/accounts/login/',
            '/accounts/register/',
            '/accounts/logout/',
            '/accounts/google/',
            '/admin/',
            '/static/',
            '/media/',
        )
        return not path.startswith(excluded_prefixes)
