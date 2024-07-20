from collections import namedtuple as nt
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from apps.user.models import User

from .conftest import DataType, UserSchema

# ----- GoogleOAuth2 Test Case Schemas ---------------------------------------------------------------------------------
R_TestCase = nt("RedirectGoogleOAuth2", ["auth_user", "expected_status", "expected_data"])
G_TestCase = nt("GoogleOAuth2", ["auth_user", "user_data", "is_active", "expected_status", "expected_data"])

# ----- GoogleOAuth2 Test Cases ----------------------------------------------------------------------------------------
google_oauth2_redirect_test_cases = [
    # "auth_user", "expected_status", "expected_data"
    R_TestCase("admin", status.HTTP_200_OK, ["auth_url"]),
    R_TestCase("user1", status.HTTP_403_FORBIDDEN, ["detail"]),
]
google_oauth2_callback_test_cases = [
    # "auth_user", "user_data", "expected_status", "expected_data"
    G_TestCase("admin", "valid_data", True, status.HTTP_200_OK, ["user", "access", "refresh"]),
    G_TestCase("admin", "invalid_data", True, status.HTTP_400_BAD_REQUEST, ["detail"]),
    G_TestCase("admin", "valid_data", False, status.HTTP_403_FORBIDDEN, ["detail"]),
    G_TestCase("user1", "valid_data", True, status.HTTP_403_FORBIDDEN, ["detail"]),
]


# ----- GoogleOAuth2 Tests ---------------------------------------------------------------------------------------------
@pytest.mark.django_db
class TestGoogleOAuth2:

    model = User

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, auth_client, users, user_data):
        self.auth_client = auth_client
        self.users: UserSchema = users
        self.google_oauth2_data: DataType = user_data.get("google_oauth2")

    # ----- RedirectView to Google OAuth2 ------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", google_oauth2_redirect_test_cases)
    def test_redirect_view_to_google_oauth2(self, test_case: R_TestCase):
        client = self.get_testcase_client(test_case.auth_user)
        response = client.get(reverse("google-login"))

        assert response.status_code == test_case.expected_status
        for key in test_case.expected_data:
            assert key in response.data

    # ----- Google OAuth2 ----------------------------------------------------------------------------------------------
    @patch("apps.user_auth.helpers.load_backend")
    @pytest.mark.parametrize("test_case", google_oauth2_callback_test_cases)
    def test_google_oauth2_callback(self, mock_load_backend, test_case: G_TestCase):
        mock_load_backend.return_value.complete.side_effect = lambda: self.mock_complete(test_case)

        url = reverse("google-login-complete")
        data = getattr(self.google_oauth2_data, test_case.user_data)
        client = self.get_testcase_client(test_case.auth_user)

        response = client.post(url, data=data)

        assert response.status_code == test_case.expected_status
        for key in test_case.expected_data:
            assert key in response.data

    # ----- Helper Methods ---------------------------------------------------------------------------------------------
    def get_testcase_client(self, auth_user):
        return self.auth_client(getattr(self.users, auth_user))

    def mock_complete(self, testcase):
        if testcase.user_data == "invalid_data":
            raise Exception("Authentication failed")
        return self.model.objects.create(email="user@example.com", is_active=testcase.is_active)
