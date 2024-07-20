import pytest


@pytest.mark.django_db
def test_user_str_method(users):
    user = users.user1
    assert str(user) == user.email
