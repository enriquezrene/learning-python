from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from src.models.task_model import TaskModel
from src.tasks.task_domain import Task


class TaskRepository:
    def __init__(self, session_factory: sessionmaker):
        self.Session = session_factory

    def create(self, task: Task):
        with self.Session() as session:
            db_task = TaskModel.from_entity(task)
            session.add(db_task)
            session.commit()

    def update(self, task: Task):
        with self.Session() as session:
            db_task = session.get(TaskModel, task.id)

            if not db_task:
                raise ValueError(f"Task with ID {task.id} not found.")

            db_task.title = task.title
            db_task.description = task.description
            db_task.status = task.status

            session.commit()

    def delete(self, task_id):
        with self.Session() as session:
            db_task = session.get(TaskModel, task_id)
            if not db_task:
                raise ValueError(f"Task with ID {task_id} not found.")
            session.delete(db_task)
            session.commit()

    def get_by_id(self, task_id):
        with self.Session() as session:
            db_task = session.get(TaskModel, task_id)
            return db_task.to_entity() if db_task else None

    def get_all(self, status=None, search_term=None):
        with self.Session() as session:
            query = select(TaskModel)
            if status:
                query = query.where(TaskModel.status == status)
            if search_term:
                query = query.where(TaskModel.title.ilike(f"%{search_term}%"))

            result = session.scalars(query).all()
            return [db_task.to_entity() for db_task in result]