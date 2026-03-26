
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.socialaccount.models import SocialApp
from .forms import TeacherRegisterForm, TeacherProfileForm
from .models import TeacherProfile


def is_google_login_enabled(request):
    return 'allauth.socialaccount.providers.google' in getattr(settings, 'INSTALLED_APPS', [])


def ensure_google_social_app(request):
    """Ensure Google SocialApp exists and is linked to the current Site when env creds are available."""
    if not is_google_login_enabled(request):
        return False

    client_id = (getattr(settings, 'GOOGLE_CLIENT_ID', '') or '').strip()
    client_secret = (
        getattr(settings, 'GOOGLE_CLIENT_SECRET', '') or '').strip()
    if not (client_id and client_secret):
        return False

    current_site = get_current_site(request)
    app = SocialApp.objects.filter(
        provider='google', client_id=client_id).first()
    if app is None:
        app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id=client_id,
            secret=client_secret,
            key='',
        )
    elif app.secret != client_secret:
        app.secret = client_secret
        app.save(update_fields=['secret'])

    if not app.sites.filter(pk=current_site.pk).exists():
        app.sites.add(current_site)

    return True


class GoogleStartView(View):
    def get(self, request):
        try:
            configured = ensure_google_social_app(request)
        except Exception:
            configured = False

        if not configured:
            messages.error(
                request,
                'Google login is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.',
            )
            return redirect('accounts:login')

        return redirect('/accounts/google/login/')


class TeacherLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_login_enabled'] = is_google_login_enabled(self.request)
        return context


class RootRedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, 'landing.html')


class RegisterView(View):

    def get(self, request):
        form = TeacherRegisterForm()
        return render(request, 'accounts/register.html', {
            'form': form,
            'google_login_enabled': is_google_login_enabled(request),
        })

    def post(self, request):
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {
            'form': form,
            'google_login_enabled': is_google_login_enabled(request),
        })


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        profile = self._get_profile(request.user)
        form = TeacherProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {
            'form': form,
            'is_onboarding': not profile.is_complete,
        })

    def post(self, request):
        profile = self._get_profile(request.user)
        form = TeacherProfileForm(request.POST, instance=profile)
        if form.is_valid():
            saved_profile = form.save()
            self._sync_teacher_name_phone(request.user, saved_profile)
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard:home')

        return render(request, 'accounts/profile.html', {
            'form': form,
            'is_onboarding': not profile.is_complete,
        })

    def _get_profile(self, teacher):
        profile, _ = TeacherProfile.objects.get_or_create(
            teacher=teacher,
            defaults={
                'full_name': f'{teacher.first_name} {teacher.last_name}'.strip(),
                'mobile_no': (teacher.phone or '').strip(),
            },
        )
        return profile

    def _sync_teacher_name_phone(self, teacher, profile):
        parts = profile.full_name.strip().split(maxsplit=1)
        teacher.first_name = parts[0] if parts else ''
        teacher.last_name = parts[1] if len(parts) > 1 else ''
        teacher.phone = profile.mobile_no
        teacher.save(update_fields=['first_name', 'last_name', 'phone'])
