import uuid
from src.tasks.task_domain import Task, TaskStatus
from typing import Optional

from src.tasks.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(self, title, description=None, status=TaskStatus.PENDING):
        new_task = Task(title=title, description=description, status=status)
        self.repository.create(new_task)
        return new_task

    def remove_task(self, task_id: uuid.UUID) -> None:
        self.repository.delete(task_id)

    def get_task(self, task_id: uuid.UUID) -> Optional[Task]:
        return self.repository.get_by_id(task_id)

    def update_task(self, task_id: uuid.UUID, **kwargs):
        task = self.repository.get_by_id(task_id)

        if not task:
            raise ValueError(f"Task {task_id} not found")

        for key, value in kwargs.items():
            if key == "status" and isinstance(value, str):
                try:
                    value = TaskStatus(value.lower())
                except ValueError:
                    raise ValueError(f"Invalid status: {value}")
            setattr(task, key, value)

        self.repository.update(task)
        return task

    def list_tasks(self, status=None, search_term=None):
        return self.repository.get_all(status=status, search_term=search_term)