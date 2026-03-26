from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Auto-sign up social users and connect existing users by email."""

    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        email = (sociallogin.user.email or '').strip().lower()
        if not email:
            return

        user_model = get_user_model()
        try:
            existing_user = user_model.objects.get(email__iexact=email)
        except user_model.DoesNotExist:
            return

        sociallogin.connect(request, existing_user)
