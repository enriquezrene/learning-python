import os, uuid
from src.task import Task, TaskStatus
from src.storage import CSVStorage


def test_save_tasks_to_csv():
    filename = "test_tasks.csv"
    storage = CSVStorage(filename)
    tasks = [
        Task(title="Buy milk", status=TaskStatus.PENDING),
        Task(title="Clean room", status=TaskStatus.DONE)
    ]

    storage.save(tasks)

    assert os.path.exists(filename)
    os.remove(filename)


def test_load_tasks_from_csv():
    filename = "test_load.csv"
    storage = CSVStorage(filename)

    with open(filename, "w") as f:
        f.write("id,title,description,status\n")
        f.write(f"{uuid.uuid4()},Buy bread,,pending\n")

    tasks = storage.load()

    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)
    assert isinstance(tasks[0].id, uuid.UUID)
    assert isinstance(tasks[0].status, TaskStatus)
    assert tasks[0].title == "Buy bread"

    os.remove(filename)