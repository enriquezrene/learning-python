from sqlalchemy import String, Uuid, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from src.tasks.task_domain import Task, TaskStatus
import uuid
from src.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus, name="task_status"), default=TaskStatus.PENDING)

    @classmethod
    def from_entity(cls, task: Task):
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status
        )

    def to_entity(self) -> Task:
        return TaskModel(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status
        )