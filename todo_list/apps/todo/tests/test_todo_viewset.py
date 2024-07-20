from collections import namedtuple as nt
from datetime import datetime, timezone

import pytest
from django.urls import reverse
from rest_framework import status

from apps.todo.models import Todo as TodoModel

from .conftest import TodoSchema, UserSchema

# ----- TodoViewSet Test Case Schemas ----------------------------------------------------------------------------------
L_TestCase = nt("List", ["auth_user", "user", "expected_result", "expected_status"])
C_TestCase = nt("Create", ["auth_user", "user", "include_optional_fields", "expected_status"])
R_TestCase = nt("Retrieve", ["auth_user", "todo", "expected_status"])
U_TestCase = nt("Update", ["auth_user", "todo", "invalid_data", "include_optional_fields", "expected_status"])
P_TestCase = nt("PartialUpdate", ["auth_user", "todo", "expected_status"])
D_TestCase = nt("Destroy", ["auth_user", "todo", "expected_status"])

# ----- TodoViewSet Test Cases -----------------------------------------------------------------------------------------
list_todo_test_cases = [
    # "auth_user", "user", "expected_result", "expected_status"
    L_TestCase("not_auth", "user1", None, status.HTTP_401_UNAUTHORIZED),
    L_TestCase("admin", "admin", 0, status.HTTP_200_OK),
    L_TestCase("admin", "user1", 1, status.HTTP_200_OK),
    L_TestCase("user1", "user1", 1, status.HTTP_200_OK),
    L_TestCase("user1", "user2", None, status.HTTP_403_FORBIDDEN),
]
create_todo_test_cases = [
    # "auth_user", "user", "include_optional_fields", "expected_status"
    C_TestCase("not_auth", "user1", False, status.HTTP_401_UNAUTHORIZED),
    C_TestCase("admin", "user1", False, status.HTTP_201_CREATED),
    C_TestCase("user1", "user1", False, status.HTTP_201_CREATED),
    C_TestCase("user1", "user1", True, status.HTTP_201_CREATED),
    C_TestCase("user1", "user2", False, status.HTTP_403_FORBIDDEN),
]
retrieve_todo_test_cases = [
    # "auth_user", "to-do", "expected_status"
    R_TestCase("not_auth", "todo__user1", status.HTTP_401_UNAUTHORIZED),
    R_TestCase("admin", "todo__user1", status.HTTP_200_OK),
    R_TestCase("user1", "todo__user1", status.HTTP_200_OK),
    R_TestCase("user1", "todo__user2", status.HTTP_403_FORBIDDEN),
]
update_todo_test_cases = [
    # "auth_user", "to-do", "invalid_data", "include_optional_fields", "expected_status"
    U_TestCase("not_auth", "todo__user1", False, False, status.HTTP_401_UNAUTHORIZED),
    U_TestCase("admin", "todo__user1", False, False, status.HTTP_200_OK),
    U_TestCase("user1", "todo__user1", False, True, status.HTTP_200_OK),
    U_TestCase("user1", "todo__user1", True, True, status.HTTP_400_BAD_REQUEST),
    U_TestCase("user1", "todo__user2", False, False, status.HTTP_403_FORBIDDEN),
]
partial_update_todo_test_cases = [
    # "auth_user", "to-do", "expected_status"
    P_TestCase("not_auth", "todo__user1", status.HTTP_401_UNAUTHORIZED),
    P_TestCase("admin", "todo__user1", status.HTTP_200_OK),
    P_TestCase("user1", "todo__user1", status.HTTP_200_OK),
    P_TestCase("user1", "todo__user2", status.HTTP_403_FORBIDDEN),
]
destroy_todo_test_cases = [
    # "auth_user", "to-do", "expected_status"
    D_TestCase("not_auth", "todo__user1", status.HTTP_401_UNAUTHORIZED),
    D_TestCase("admin", "todo__user1", status.HTTP_204_NO_CONTENT),
    D_TestCase("user1", "todo__user1", status.HTTP_204_NO_CONTENT),
    D_TestCase("user1", "todo__user2", status.HTTP_403_FORBIDDEN),
]


# ----- TodoViewSet Tests ----------------------------------------------------------------------------------------------
@pytest.mark.django_db
class TestTodoViewSet:

    model = TodoModel

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, auth_client, users, todos, testcase_data):
        self.client = auth_client
        self.users: UserSchema = users
        self.todo: TodoSchema = todos

        self.create_data = testcase_data.get("todo").for_create
        self.update_data = testcase_data.get("todo").for_update
        self.invalid_update_data = testcase_data.get("todo").for_invalid_update
        self.partial_update_data = testcase_data.get("todo").for_partial_update
        self.optional_fields = testcase_data.get("todo").optional_fields

    # ----- List To-do -------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", list_todo_test_cases)
    def test_list_todo(self, test_case: L_TestCase):
        client, user = self.get_testcase_client_and_user(test_case)

        url = reverse("todo-list", kwargs={"user_id": user.id})
        response = client.get(url)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_200_OK:
            result = response.data["results"]
            assert isinstance(result, list)
            assert len(result) == test_case.expected_result
            assert response.data["count"] == self.initial_todo_count(user)

    # ----- Create To-do -----------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", create_todo_test_cases)
    def test_create_todo(self, test_case: C_TestCase):
        client, user = self.get_testcase_client_and_user(test_case)
        todos_count = self.initial_todo_count(user)

        url = reverse("todo-list", kwargs={"user_id": user.id})
        data = self.get_data(self.create_data, test_case.include_optional_fields)
        response = client.post(url, data=data)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_201_CREATED:
            assert self.model.objects.filter(user=user).count() == todos_count + 1

    # ----- Retrieve To-do ---------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", retrieve_todo_test_cases)
    def test_retrieve_todo(self, test_case: R_TestCase):
        client, todo = self.get_testcase_client_and_todo(test_case)

        url = reverse("todo-detail", kwargs={"user_id": todo.user.id, "pk": todo.id})
        response = client.get(url)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_200_OK:
            assert response.data.get("title") == todo.title

    # ----- Update To-do -----------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", update_todo_test_cases)
    def test_update_todo(self, test_case: U_TestCase):
        client, todo = self.get_testcase_client_and_todo(test_case)

        url = reverse("todo-detail", kwargs={"user_id": todo.user.id, "pk": todo.id})
        update_data = self.update_data if not test_case.invalid_data else self.invalid_update_data
        data = self.get_data(update_data, test_case.include_optional_fields)
        response = client.put(url, data=data)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_200_OK:
            self.verify_todo_fields(todo.id, data)

    # ----- Partial Update To-do ---------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", partial_update_todo_test_cases)
    def test_partial_update_todo(self, test_case: P_TestCase):
        client, todo = self.get_testcase_client_and_todo(test_case)

        url = reverse("todo-detail", kwargs={"user_id": todo.user.id, "pk": todo.id})
        data = self.partial_update_data
        response = client.patch(url, data=data)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_200_OK:
            self.verify_todo_fields(todo.id, data)

    # ----- Destroy To-do ----------------------------------------------------------------------------------------------
    @pytest.mark.parametrize("test_case", destroy_todo_test_cases)
    def test_destroy_todo(self, test_case: D_TestCase):
        client, todo = self.get_testcase_client_and_todo(test_case)
        todos_count = self.initial_todo_count(todo.user)

        url = reverse("todo-detail", kwargs={"user_id": todo.user.id, "pk": todo.id})
        response = client.delete(url)

        assert response.status_code == test_case.expected_status
        if test_case.expected_status == status.HTTP_204_NO_CONTENT:
            assert self.model.objects.filter(id=todo.id).first() is None
            assert self.model.objects.filter(user=todo.user).count() == todos_count - 1

    # ----- Helper Methods ---------------------------------------------------------------------------------------------
    def initial_todo_count(self, user):
        return self.model.objects.filter(user=user).count()

    def get_testcase_client(self, test_case):
        return self.client(getattr(self.users, test_case.auth_user))

    def get_testcase_user(self, test_case):
        return getattr(self.users, test_case.user)

    def get_testcase_task(self, test_case):
        return getattr(self.todo, test_case.todo)

    def get_testcase_client_and_user(self, test_case):
        client = self.get_testcase_client(test_case)
        user = self.get_testcase_user(test_case)
        return client, user

    def get_testcase_client_and_todo(self, test_case):
        client = self.get_testcase_client(test_case)
        todo = self.get_testcase_task(test_case)
        return client, todo

    def get_data(self, data: dict, optional_fields: bool = False):
        if optional_fields:
            data.update(self.optional_fields)
        return data

    def verify_todo_fields(self, todo_id: int, data: dict):
        todo = self.model.objects.get(id=todo_id)
        for field, value in data.items():
            todo_value = getattr(todo, field)
            if isinstance(todo_value, datetime):
                value = value.replace(tzinfo=timezone.utc)
            assert todo_value == value
