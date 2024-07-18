from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from apps.user.models import User

from .models import EmailVerificationToken


@shared_task
def clean_blacklist():
    current_time = timezone.localtime(timezone.now())

    # Removing obsolete tokens from BlacklistedToken
    blacklisted_expired_tokens = BlacklistedToken.objects.filter(token__expires_at__lte=current_time)  # type: ignore
    blacklisted_expired_tokens.delete()

    # Removing obsolete tokens from OutstandingToken
    outstanding_expired_tokens = OutstandingToken.objects.filter(expires_at__lte=current_time)  # type: ignore
    outstanding_expired_tokens.delete()


@shared_task
def send_verification_email(user_id: int):
    try:
        user = User.objects.get(id=user_id)
        token, created = EmailVerificationToken.objects.get_or_create(user=user)

        if token.is_expired():
            token.delete()
            token = EmailVerificationToken.objects.create(user=user)

        verification_link = f"{settings.BASE_FRONTEND_URL}/verify/email/{token.token}/"
        send_mail(
            subject="Verify your email address",
            message=f"Click the link to verify your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    except User.DoesNotExist:  # type: ignore
        pass


@shared_task
def delete_expired_users():
    current_time = timezone.localtime(timezone.now())
    expiration_date = current_time - timedelta(days=1)
    tokens = EmailVerificationToken.objects.filter(created_at__lt=expiration_date)

    for token in tokens:
        user = token.user
        if not user.is_email_verified:
            user.delete()
