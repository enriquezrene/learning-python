from http.client import HTTPException

from flask import Flask, jsonify

from src.database import SessionLocal
from src.tasks.task_repository import TaskRepository
from src.tasks.task_routes import tasks_bp
from src.tasks.task_service import TaskService


def create_app():
    app = Flask(__name__)

    # DI
    task_repository = TaskRepository(session_factory=SessionLocal)
    todo_service = TaskService(repository=task_repository)

    # Attach service to app config so the Blueprint can find it
    app.config['TODO_SERVICE'] = todo_service

    # Register the "Feature"
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
