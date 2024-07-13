from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView

from apps.user_auth.helpers import get_token_pair
from apps.user_auth.serializers import SignupSerializer


class SignupAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token_pair = get_token_pair(user)

        response_data = {"user": serializer.data, **token_pair}
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]


class LogoutAPIView(TokenBlacklistView):
    permission_classes = [AllowAny]
