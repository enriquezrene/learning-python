import uuid
from src.todo_list import TodoList
from src.task import Task, TaskStatus
from unittest.mock import MagicMock


def test_list_tasks_filter_and_search():
    todo = TodoList()
    todo.add_task("Buy bread", status=TaskStatus.PENDING)
    todo.add_task("Buy milk", status=TaskStatus.DONE)
    todo.add_task("Clean room", status=TaskStatus.PENDING)

    results = todo.list_tasks(status=TaskStatus.PENDING, search_term="Buy")

    assert len(results) == 1
    assert results[0].title == "Buy bread"

def test_search_tasks_by_keyword():
    todo = TodoList()
    todo.add_task("Buy groceries")
    todo.add_task("Clean the car")

    results = todo.list_tasks(search_term="car")

    assert len(results) == 1
    assert "car" in results[0].title

def test_list_tasks_with_filter():
    todo = TodoList()
    todo.add_task("Task 1", status=TaskStatus.PENDING)
    todo.add_task("Task 2", status=TaskStatus.DONE)

    pending_tasks = todo.list_tasks(status=TaskStatus.PENDING)

    assert len(pending_tasks) == 1
    assert pending_tasks[0].title == "Task 1"

def test_todo_list_saves_on_add():
    mock_storage = MagicMock()
    todo = TodoList(storage=mock_storage)

    todo.add_task("Test DI")

    assert mock_storage.save.called


def test_get_task_by_id():
    todo = TodoList()
    task = todo.add_task("Find me")

    found_task = todo.get_task(task.id)

    assert found_task is not None
    assert found_task.id == task.id
    assert found_task.title == "Find me"


def test_get_task_returns_none_if_not_found():
    todo = TodoList()
    non_existent_id = uuid.uuid4()

    found_task = todo.get_task(non_existent_id)

    assert found_task is None


def test_add_task_returns_task_object():
    todo = TodoList()

    task = todo.add_task("Test return value")

    assert isinstance(task, Task)
    assert task.title == "Test return value"

    todo.remove_task(task.id)
    assert len(todo.tasks) == 0


def test_add_task_to_list():
    todo = TodoList()

    todo.add_task("Buy groceries")

    assert len(todo.tasks) == 1
    assert todo.tasks[0].title == "Buy groceries"
    assert isinstance(todo.tasks[0], Task)


def test_remove_task_by_id():
    todo = TodoList()
    todo.add_task("Task to delete")
    task_id = todo.tasks[0].id

    todo.remove_task(task_id)

    assert len(todo.tasks) == 0
