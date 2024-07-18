from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.user_auth.helpers import OAuth2Redirect, get_backend, get_token_pair

from .serializers import GoogleOAuth2Serializer


class GoogleOAuth2Redirect(OAuth2Redirect):
    redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
    service_name = settings.GOOGLE_OAUTH2_SERVICE_NAME


class GoogleOAuth2CallbackView(CreateAPIView):
    """Exchange google code for user data and JSON web token pair."""

    redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
    service_name = settings.GOOGLE_OAUTH2_SERVICE_NAME
    serializer_class = GoogleOAuth2Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        backend = get_backend(request, self.service_name, self.redirect_uri)
        backend.data = serializer.validated_data

        try:
            user = backend.complete()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            user.is_email_verified = True
            user.save()

            token_pair = get_token_pair(user)
            serializer = self.get_serializer({"user": user, **token_pair})
            return Response(serializer.data)

        return Response({"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
