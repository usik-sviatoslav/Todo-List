from .google_oauth2 import settings as google_oauth2
from .jwt_auth import settings as jwt_auth

__all__ = [
    "jwt_auth",
    "google_oauth2",
]
