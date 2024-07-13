from django.urls import include, path

from .jwt_auth.urls import urlpatterns as jwt_auth

urlpatterns = [
    path("", include(jwt_auth), name="jwt_auth"),
]
