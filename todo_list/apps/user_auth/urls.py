from django.urls import include, path

from .google_oauth2.urls import urlpatterns as google_oauth2
from .jwt_auth.urls import urlpatterns as jwt_auth

urlpatterns = [
    path("", include(jwt_auth), name="jwt_auth"),
    path("", include(google_oauth2), name="google_oauth2"),
]
