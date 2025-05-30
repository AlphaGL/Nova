from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.email = data.get('email')
        user.name = data.get('name') or user.name  # optional
        return user

    def pre_social_login(self, request, sociallogin):
        # Skip if user already logged in
        if request.user.is_authenticated:
            return

        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                perform_login(request, user, email_verification='optional')
            except User.DoesNotExist:
                pass  # Let Allauth handle sign-up
