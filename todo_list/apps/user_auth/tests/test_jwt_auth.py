import uuid
from collections import namedtuple as nt
from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from apps.user_auth.models import EmailVerificationToken

from .conftest import DataType, UserSchema

# ----- JWTAuth Test Case Schemas --------------------------------------------------------------------------------------
S_TestCase = nt("Signup", ["user_data", "expected_status", "expected_data"])
V_TestCase = nt("VerifyEmail", ["auth_user", "user", "token", "expected_status", "expected_data"])
L_TestCase = nt("Login", ["auth_user", "user_data", "is_email_verified", "expected_status", "expected_data"])
O_TestCase = nt("Logout", ["auth_user", "refresh_token", "expected_status", "expected_data"])

# ----- JWTAuth Test Cases ---------------------------------------------------------------------------------------------
signup_test_cases = [
    # "user_data", "expected_status", "expected_data"
    S_TestCase("valid_data", status.HTTP_201_CREATED, "Please check your email to verify your account."),
    S_TestCase("invalid_data", status.HTTP_400_BAD_REQUEST, None),
]
verify_email_test_cases = [
    # "auth_user", "user", "token", "expected_status", "expected_data"
    V_TestCase("admin", "user1", "valid_token", status.HTTP_200_OK, "Email verified successfully."),
    V_TestCase("admin", "user1", "invalid_token", status.HTTP_404_NOT_FOUND, "not_found"),
    V_TestCase("admin", "user1", "expired_token", status.HTTP_400_BAD_REQUEST, "invalid"),
    V_TestCase("user1", "user1", "valid_token", status.HTTP_403_FORBIDDEN, "permission_denied"),
]
login_test_cases = [
    # "auth_user", "user_data", "is_email_verified", "expected_status", "expected_data"
    L_TestCase("user1", "valid_data", True, status.HTTP_200_OK, ["access", "refresh"]),
    L_TestCase("user1", "valid_data", False, status.HTTP_403_FORBIDDEN, "permission_denied"),
    L_TestCase("user1", "invalid_data", False, status.HTTP_401_UNAUTHORIZED, "no_active_account"),
]
logout_test_cases = [
    # "auth_user", "refresh_token", "expected_status"
    O_TestCase("user1", "valid_token", status.HTTP_200_OK, ""),
    O_TestCase("user1", "expired_token", status.HTTP_401_UNAUTHORIZED, "token_not_valid"),
]


# ----- JWTAuth Tests ----------------------------------------------------------------------------------------------
@pytest.mark.django_db
class TestJWTAuth:

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, client, auth_client, users, user_data):
        self.client = client
        self.auth_client = auth_client
        self.users: UserSchema = users

        self.sign_up_data: DataType = user_data.get("sign_up")
        self.login_data: DataType = user_data.get("login")

    # ----- Signup User ------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", signup_test_cases)
    def test_signup(self, test_case: S_TestCase):
        url = reverse("sign-up")
        data = getattr(self.sign_up_data, test_case.user_data)
        response = self.client.post(url, data=data)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_201_CREATED:
            assert response.data.get("message") == test_case.expected_data
            assert User.objects.filter(email=data.get("email")).exists()

    # ----- Verify Email -----------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", verify_email_test_cases)
    def test_verify_email(self, test_case: V_TestCase):
        client = self.get_testcase_client(test_case.auth_user)
        user = getattr(self.users, test_case.user)
        token = EmailVerificationToken.objects.create(user=user)

        if test_case.token == "invalid_token":
            token.token = uuid.uuid4()
        if test_case.token == "expired_token":
            token.created_at = token.created_at - timedelta(days=2)
            token.save()

        url = reverse("verify-email", kwargs={"token": token.token})
        response = client.post(url)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_200_OK:
            assert response.data.get("detail") == test_case.expected_data
            user.refresh_from_db()
            assert user.is_email_verified
        else:
            assert response.data.get("detail").code == test_case.expected_data

    # ----- Login User -------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", login_test_cases)
    def test_login(self, test_case: L_TestCase):
        user = getattr(self.users, test_case.auth_user)
        user.is_email_verified = test_case.is_email_verified
        user.save()

        url = reverse("login")
        data = getattr(self.login_data, test_case.user_data)
        response = self.client.post(url, data=data)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_200_OK:
            for key in test_case.expected_data:
                assert key in response.data
        else:
            assert response.data.get("detail").code == test_case.expected_data

    # ----- Logout User ------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", logout_test_cases)
    def test_logout(self, test_case: O_TestCase):
        user = getattr(self.users, test_case.auth_user)
        token = RefreshToken.for_user(user)

        if test_case.refresh_token == "expired_token":
            token.set_exp(lifetime=-timedelta(days=1))

        url = reverse("logout")
        data = {"refresh": str(token)}
        response = self.client.post(url, data=data)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status != status.HTTP_200_OK:
            assert response.data.get("detail").code == test_case.expected_data

    # ----- Helper Methods ---------------------------------------------------------------------------------------------
    def get_testcase_client(self, auth_user):
        return self.auth_client(getattr(self.users, auth_user))
