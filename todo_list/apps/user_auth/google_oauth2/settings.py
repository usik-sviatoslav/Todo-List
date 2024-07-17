import os

from django.conf import settings

settings.INSTALLED_APPS += [
    "social_django",
    "apps.user_auth.google_oauth2",
]

settings.AUTHENTICATION_BACKENDS += [
    "social_core.backends.google.GoogleOAuth2",
]

settings.SOCIAL_AUTH_SESSION_COOKIE = False
settings.SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
settings.SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_OAUTH2_KEY")
settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_OAUTH2_SECRET")
settings.GOOGLE_OAUTH2_REDIRECT_URI = os.getenv("GOOGLE_OAUTH2_REDIRECT_URI")
settings.GOOGLE_OAUTH2_SERVICE_NAME = "google-oauth2"

if settings.DEBUG:
    settings.SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
