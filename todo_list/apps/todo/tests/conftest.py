from collections import namedtuple
from datetime import datetime, timedelta

import pytest

from core.conftest import TodoSchema, UserSchema, api_client, auth_client, django_db_setup, todos, users  # noqa: F401

# ----- Data Fixtures --------------------------------------------------------------------------------------------------
DataType = namedtuple(
    "DataType", ["for_create", "for_update", "for_invalid_update", "for_partial_update", "optional_fields"]
)


@pytest.fixture
def testcase_data():
    due_date = datetime.now() + timedelta(days=1)
    due_date = due_date.replace(hour=16, minute=0, second=0, microsecond=0)

    data = {
        "todo": DataType(
            for_create={"title": "New Todo", "due_date": due_date},
            for_update={"title": "Updated Todo", "due_date": due_date + timedelta(days=1)},
            for_invalid_update={"title": "Updated Todo", "due_date": due_date - timedelta(days=5)},
            for_partial_update={"description": "New Todo Description"},
            optional_fields={"description": "Todo Description", "completed": True},
        ),
    }
    return data
