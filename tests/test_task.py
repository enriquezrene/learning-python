import uuid
from src.task import Task, TaskStatus


def test_task_has_unique_uuid():
    task1 = Task(title="First Task")
    task2 = Task(title="Second Task")

    assert task1.id is not None
    assert isinstance(task1.id, uuid.UUID)
    assert task1.id != task2.id

def test_task_has_defaults():
    task = Task(title="New Task")
    assert task.status == TaskStatus.PENDING
    assert task.description == ""

def test_task_with_custom_values():
    task = Task(
        title="Complex Task",
        description="This is a long description",
        status=TaskStatus.IN_PROGRESS
    )
    assert task.description == "This is a long description"
    assert task.status == TaskStatus.IN_PROGRESS


def test_task_can_be_marked_completed():
    task = Task(title="Clean the kitchen")

    task.status = TaskStatus.DONE

    assert task.status is TaskStatus.DONE