import uuid

from sqlalchemy.exc import SQLAlchemyError
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

    def remove_task(self, task_id: uuid.UUID) -> bool:
        return self.repository.delete(task_id)

    def get_task(self, task_id: uuid.UUID) -> Optional[Task]:
        return self.repository.get_by_id(task_id)

    def update_task(self, task_id: uuid.UUID, **kwargs):
        try:
            task = self.repository.get_by_id(task_id)

            if not task:
                return None

            for key, value in kwargs.items():
                if hasattr(task, key):
                    # Handle Enum conversion logic
                    if key == "status" and isinstance(value, str):
                        value = TaskStatus(value.lower())
                    setattr(task, key, value)

            self.repository.update(task)
            return task
        except ValueError as e:
            raise e
        except SQLAlchemyError:
            raise RuntimeError("Database operation failed")

    def list_tasks(self, status=None, search_term=None):
        if isinstance(status, str):
            try:
                status = TaskStatus(status.lower())
            except ValueError:
                raise ValueError(f"'{status}' is not a valid task status")
        return self.repository.get_all(status=status, search_term=search_term)