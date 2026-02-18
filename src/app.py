import os

from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.tasks.task_repository import TaskRepository
from src.tasks.task_service import TaskService


def create_app(task_service: TaskService = None):
    app = Flask(__name__)
    CORS(app)

    # If NO service is provided, we build the production version
    if task_service is None:
        # Render provides DATABASE_URL
        db_url = os.getenv("DATABASE_URL", "sqlite:///app.db")

        # SQLAlchemy 1.4+ fix for Render's 'postgres://' prefix
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        engine = create_engine(db_url)
        session_factory = sessionmaker(bind=engine)
        repo = TaskRepository(session_factory=session_factory)
        task_service = TaskService(repository=repo)

    app.config['TASK_SERVICE'] = task_service

    # Register your blueprints here
    from src.tasks.task_routes import tasks_bp
    app.register_blueprint(tasks_bp)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code

        return jsonify({
            "error": "An unexpected server error occurred.",
            "type": e.__class__.__name__
        }), 500

    return app
