from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LoginAPIView, LogoutAPIView, SignupAPIView

SchemaTag = "JWT Authentication"

LoginAPIView = extend_schema(tags=[SchemaTag])(LoginAPIView)
LogoutAPIView = extend_schema(tags=[SchemaTag])(LogoutAPIView)
SignupAPIView = extend_schema(tags=[SchemaTag], auth=[])(SignupAPIView)
TokenObtainPairView = extend_schema(tags=[SchemaTag])(TokenObtainPairView)
TokenRefreshView = extend_schema(tags=[SchemaTag])(TokenRefreshView)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("sign-up/", SignupAPIView.as_view(), name="sign-up"),
    path("token/obtain/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
