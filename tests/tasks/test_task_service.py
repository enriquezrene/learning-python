import uuid
import pytest

from src.tasks.task_service import TaskService
from src.models.task_model import Task, TaskStatus
from unittest.mock import MagicMock

from src.tasks.task_repository import TaskRepository  # Ensure this matches your file name


@pytest.fixture
def task_service(test_db):
    repo = TaskRepository(session_factory=test_db)
    return TaskService(repo)

def test_list_tasks_filter_and_search(task_service):
    task_service.add_task("Buy bread", status=TaskStatus.PENDING)
    task_service.add_task("Buy milk", status=TaskStatus.DONE)
    task_service.add_task("Clean room", status=TaskStatus.PENDING)

    results = task_service.list_tasks(status=TaskStatus.PENDING, search_term="Buy")

    assert len(results) == 1
    assert results[0].title == "Buy bread"

def test_search_tasks_by_keyword(task_service):
    task_service.add_task("Buy groceries")
    task_service.add_task("Clean the car")

    results = task_service.list_tasks(search_term="car")

    assert len(results) == 1
    assert "car" in results[0].title

def test_list_tasks_with_filter(task_service):
    task_service.add_task("Task 1", status=TaskStatus.PENDING)
    task_service.add_task("Task 2", status=TaskStatus.DONE)

    pending_tasks = task_service.list_tasks(status=TaskStatus.PENDING)

    assert len(pending_tasks) == 1
    assert pending_tasks[0].title == "Task 1"

def test_get_task_by_id(task_service):
    task = task_service.add_task("Find me")

    found_task = task_service.get_task(task.id)

    assert found_task is not None
    assert found_task.id == task.id
    assert found_task.title == "Find me"


def test_get_task_returns_none_if_not_found(task_service):
    non_existent_id = uuid.uuid4()

    found_task = task_service.get_task(non_existent_id)

    assert found_task is None
