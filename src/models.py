from sqlalchemy import String, Uuid, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.task import TaskStatus, Task
import uuid

class Base(DeclarativeBase):
    pass

class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)

    @classmethod
    def from_entity(cls, task: Task):
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status
        )

    def to_entity(self) -> Task:
        return Task(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status
        )