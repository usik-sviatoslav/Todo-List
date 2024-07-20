from datetime import timedelta
from unittest.mock import patch

import pytest
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from apps.user.models import User as UserModel
from apps.user_auth.jwt_auth.tasks import clean_blacklist, delete_expired_users, send_verification_email
from apps.user_auth.models import EmailVerificationToken


@pytest.mark.django_db
def test_clean_blacklist():
    expires_at = timezone.now() - timedelta(days=1)
    outstanding_token = OutstandingToken.objects.create(token="valid_token", expires_at=expires_at)  # type: ignore
    BlacklistedToken.objects.create(token=outstanding_token)  # type: ignore

    clean_blacklist.apply()

    assert not BlacklistedToken.objects.filter(id=outstanding_token.id).exists()  # type: ignore
    assert not OutstandingToken.objects.filter(id=outstanding_token.id).exists()  # type: ignore


@pytest.mark.django_db
def test_send_verification_email(users):
    with patch("apps.user_auth.jwt_auth.tasks.send_mail") as mock_send_mail:
        send_verification_email.apply(args=[users.user1.id])
        mock_send_mail.assert_called_once()
        mail_kwargs = mock_send_mail.call_args.kwargs

        token = EmailVerificationToken.objects.get(user=users.user1)
        verification_link = f"{settings.BASE_FRONTEND_URL}/verify/email/{token.token}/"

        assert "Verify your email address" in mail_kwargs["subject"]
        assert verification_link in mail_kwargs["message"]


@pytest.mark.django_db
def test_delete_expired_users(users):
    token = EmailVerificationToken.objects.create(user=users.user1)
    token.created_at = timezone.now() - timedelta(days=1)

    assert UserModel.objects.filter(id=users.user1.id).exists()

    delete_expired_users.apply()

    assert not UserModel.objects.filter(id=users.user1.id).exists()
