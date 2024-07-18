from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_email_verified", True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(_("email"), unique=True)
    is_email_verified = models.BooleanField(default=False)
    username = models.CharField(_("username"), max_length=150)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
