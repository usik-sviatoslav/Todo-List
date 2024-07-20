from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView

from apps.user_auth.helpers import get_token_pair
from apps.user_auth.models import EmailVerificationToken
from apps.user_auth.serializers import SignupSerializer

from .tasks import send_verification_email


class SignupAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Starting a Celery task
        send_verification_email.delay(user.id)

        message = "Please check your email to verify your account."
        return Response({"user_id": user.id, "message": message}, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(APIView):
    def post(self, request, token):  # noqa
        token_obj = get_object_or_404(EmailVerificationToken, token=token)
        if token_obj.is_expired():
            raise ValidationError({"detail": "Token has expired."})

        user = token_obj.user
        user.is_email_verified = True
        user.save()

        token_obj.delete()
        token_pair = get_token_pair(user)
        return Response({"detail": "Email verified successfully.", **token_pair}, status=status.HTTP_200_OK)


class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.user.is_email_verified:
            raise PermissionDenied({"detail": "Email verification failed."})

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(TokenBlacklistView):
    permission_classes = [AllowAny]
