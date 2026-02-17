import pytest
from src.models.task_model import Task, TaskStatus
from src.tasks.task_repository import TaskRepository  # Ensure this matches your file name


@pytest.fixture
def repo(test_db):
    return TaskRepository(session_factory=test_db)


def test_create_and_fetch_task(repo):
    new_task = Task(title="Buy Milk", description="Whole milk")

    repo.create(new_task)
    fetched = repo.get_by_id(new_task.id)

    assert fetched is not None
    assert fetched.id == new_task.id
    assert fetched.title == "Buy Milk"


def test_update_task_status(repo):
    task = Task(title="Fix Bug")
    repo.create(task)

    task.status = TaskStatus.DONE
    repo.update(task)

    updated_task = repo.get_by_id(task.id)
    assert updated_task.status == TaskStatus.DONE


def test_delete_task(repo):
    task = Task(title="Temporary Task")
    repo.create(task)

    repo.delete(task.id)

    assert repo.get_by_id(task.id) is None


def test_get_all_with_filters(repo):
    repo.create(Task(title="Apple", status=TaskStatus.PENDING))
    repo.create(Task(title="Banana", status=TaskStatus.DONE))

    completed = repo.get_all(status=TaskStatus.DONE)
    assert len(completed) == 1
    assert completed[0].title == "Banana"

    search = repo.get_all(search_term="APP")
    assert len(search) == 1
    assert search[0].title == "Apple"


def test_update_non_existent_task_raises_error(repo):
    fake_task = Task(title="Ghost")
    with pytest.raises(ValueError, match="not found"):
        repo.update(fake_task)
