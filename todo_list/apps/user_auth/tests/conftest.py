from collections import namedtuple

import pytest

from core.conftest import UserSchema, api_client, auth_client, django_db_setup, users  # noqa: F401

# ----- Data Fixtures --------------------------------------------------------------------------------------------------
DataType = namedtuple("DataType", ["valid_data", "invalid_data"])


@pytest.fixture
def user_data():
    email = "user50@example.com"
    password = "TestPassword123"
    invalid_password = "InvalidTestPassword123"

    return {
        "sign_up": DataType(
            {"email": email, "password": password, "password2": password},
            {"email": email, "password": password, "password2": invalid_password},
        ),
        "login": DataType(
            {"email": "user1@gmail.com", "password": password},
            {"email": "user1@gmail.com", "password": invalid_password},
        ),
    }
