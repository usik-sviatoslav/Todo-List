from django.apps import AppConfig


class JWTAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user_auth.jwt_auth"
