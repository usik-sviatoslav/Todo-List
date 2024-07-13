from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LoginAPIView, LogoutAPIView, SignupAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("sign-up/", SignupAPIView.as_view(), name="sign-up"),
    path("token/obtain/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
