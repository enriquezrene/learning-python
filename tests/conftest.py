import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app import create_app
from src.database import Base
from src.tasks.task_service import TaskService
from src.tasks.task_repository import TaskRepository


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def test_db(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    testing_session_local = sessionmaker(bind=connection)
    yield testing_session_local

    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(test_db):
    app = create_app()
    app.config.update({"TESTING": True})

    session = test_db()
    repo = TaskRepository(session_factory=lambda: session)

    app.config['TODO_SERVICE'] = TaskService(repo)

    with app.test_client() as client:
        yield client
