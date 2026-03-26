
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from allauth.socialaccount.models import SocialApp
from .forms import TeacherRegisterForm


def is_google_login_enabled(request):
    env_configured = bool(
        getattr(settings, 'GOOGLE_CLIENT_ID', '')
        and getattr(settings, 'GOOGLE_CLIENT_SECRET', '')
    )

    socialapp_configured = False
    try:
        current_site = get_current_site(request)
        socialapp_qs = SocialApp.objects.filter(
            provider='google', sites=current_site)
        if socialapp_qs.exists():
            socialapp_configured = True
        else:
            # If a Google SocialApp exists but has no site attached, attach current site.
            app = SocialApp.objects.filter(provider='google').first()
            if app is not None:
                app.sites.add(current_site)
                socialapp_configured = True
    except Exception:
        socialapp_configured = False

    return env_configured or socialapp_configured


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
        return redirect('accounts:login')


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
