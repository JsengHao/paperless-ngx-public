import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import Http404
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import RedirectView

logger = logging.getLogger("paperless.handlers")


def raise_404(*args, **kwargs):
    raise Http404


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return reverse("base")

    def get_signup_redirect_url(self, request):
        return self.get_login_redirect_url(request)

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ENABLE_SIGNUP", False)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def authentication_error(
        self,
        request,
        provider_id,
        error=None,
        exception=None,
        extra_context=None,
    ):
        logger.error(f"Authentication error: {exception}")
        return super().authentication_error(
            request,
            provider_id,
            error,
            exception,
            extra_context,
        )

    def is_open_for_signup(self, request, sociallogin):
        # True indicates a user should be automatically created on successful
        # login via configured external provider
        return getattr(settings, "SOCIALACCOUNT_ENABLE_SIGNUP", True)


base_url = reverse_lazy("base")
urlpatterns = [
    # Override allauth URLs to disable features we don't want
    path("signup/", RedirectView.as_view(url=base_url)),
    re_path("confirm-email/.*", RedirectView.as_view(url=base_url)),
    re_path("email/.*", RedirectView.as_view(url=base_url)),
    re_path("password/.*", RedirectView.as_view(url=base_url)),
    # Import allauth-provided URL patterns
    path("", include("allauth.urls")),
]
