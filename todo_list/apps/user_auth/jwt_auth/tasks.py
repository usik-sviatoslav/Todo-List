from celery import shared_task
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


@shared_task
def clean_blacklist():
    current_time = timezone.localtime(timezone.now())

    # Removing obsolete tokens from BlacklistedToken
    blacklisted_expired_tokens = BlacklistedToken.objects.filter(token__expires_at__lte=current_time)  # type: ignore
    blacklisted_expired_tokens.delete()

    # Removing obsolete tokens from OutstandingToken
    outstanding_expired_tokens = OutstandingToken.objects.filter(expires_at__lte=current_time)  # type: ignore
    outstanding_expired_tokens.delete()

    return "Expired tokens cleaned from blacklist."
