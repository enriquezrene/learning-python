import uuid
from dataclasses import dataclass, field
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    BLOCKED = "blocked"
    DONE = "done"


@dataclass
class Task:
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    id: uuid.UUID = field(default_factory=uuid.uuid4)
