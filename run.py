import os
from src.app import create_app
from src.task_repository import TaskRepository
from src.todo_list import TodoList

db_url = os.environ.get("DATABASE_URL")
if db_url:
    task_repository = TaskRepository(db_url)
else:
    task_repository = TaskRepository("sqlite:///local_dev.db")
todo_service = TodoList(repository=task_repository)
app = create_app(todo_service=todo_service)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)