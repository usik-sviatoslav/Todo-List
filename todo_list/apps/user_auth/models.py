import uuid

from django.db import models
from django.utils import timezone

from apps.user.models import User


class EmailVerificationToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def is_expired(self):
        current_time = timezone.localtime(timezone.now())
        return (current_time - self.created_at).days > 1  # The token expires in 1 day
