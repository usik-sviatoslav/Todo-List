from datetime import timedelta

from django.conf import settings

settings.INSTALLED_APPS += [
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "apps.user_auth.jwt_auth",
]

settings.SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": settings.SECRET_KEY,
}

if settings.DEBUG:
    settings.SIMPLE_JWT.update(
        {
            "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
            "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
        }
    )
