import pytest


@pytest.mark.django_db
def test_todo_str_method(todos):
    todo = todos.todo__user1
    assert str(todo) == todo.title
