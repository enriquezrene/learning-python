import csv, uuid
from dataclasses import asdict
from src.task import Task, TaskStatus


class CSVStorage:
    def __init__(self, filename: str):
        self.filename = filename
        self.fieldnames = ["id", "title", "description", "status"]

    def save(self, tasks: list[Task]):
        with open(self.filename, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            for task in tasks:
                task_dict = asdict(task)
                task_dict["status"] = task_dict["status"].value
                writer.writerow(task_dict)

    def load(self) -> list[Task]:
        tasks = []
        try:
            with open(self.filename, mode="r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tasks.append(Task(
                        id=uuid.UUID(row["id"]),
                        title=row["title"],
                        description=row["description"],
                        status=TaskStatus(row["status"])
                    ))
        except FileNotFoundError:
            return []
        return tasks
