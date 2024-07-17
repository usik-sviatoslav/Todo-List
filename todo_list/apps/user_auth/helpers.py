from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import load_backend, load_strategy

from apps.user_auth.serializers import OAuth2RedirectSerializer


def get_backend(request, service_name, redirect_uri):
    strategy = load_strategy(request)
    redirect_uri = settings.BASE_FRONTEND_URL + redirect_uri
    return load_backend(strategy, service_name, redirect_uri=redirect_uri)


def get_token_pair(user):
    token_pair = RefreshToken.for_user(user)
    return {
        "refresh": str(token_pair),
        "access": str(token_pair.access_token),  # type: ignore
    }


class OAuth2Redirect(APIView):
    """Returns the authorization URL `auth_url`."""

    serializer_class = OAuth2RedirectSerializer
    redirect_uri, service_name = None, None

    def get(self, request):
        backend = get_backend(request, self.service_name, self.redirect_uri)
        return Response({"auth_url": backend.auth_url()})
