import uuid
from src.task import Task, TaskStatus
from typing import Optional


class TodoList:
    def __init__(self, storage=None):
        self.storage = storage
        self.tasks = self.storage.load() if self.storage else []

    def add_task(self, title: str, **kwargs) -> Task:
        new_task = Task(title=title, **kwargs)
        self.tasks.append(new_task)

        if self.storage:
            self.storage.save(self.tasks)

        return new_task

    def remove_task(self, task_id: uuid.UUID) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if self.storage:
            self.storage.save(self.tasks)

    def get_task(self, task_id: uuid.UUID) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: uuid.UUID, **kwargs):
        task = self.get_task(task_id)
        if task:
            if "status" in kwargs:
                task.status = TaskStatus(kwargs["status"])
            if "description" in kwargs:
                task.description = kwargs["description"]

            if self.storage:
                self.storage.save(self.tasks)
        return task

    def list_tasks(self, status: Optional[TaskStatus] = None, search_term: Optional[str] = None) -> list[Task]:
        filtered_tasks = self.tasks

        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status]

        if search_term:
            # case-insensitive search
            filtered_tasks = [t for t in filtered_tasks if search_term.lower() in t.title.lower()]

        return filtered_tasks