import uuid
from flask import Blueprint, jsonify, request, current_app
from src.models.task_model import TaskStatus

tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.route("/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    todo_service = current_app.config['TODO_SERVICE']
    data = request.get_json()
    try:
        target_id = uuid.UUID(task_id)
        updated_task = todo_service.update_task(target_id, **data)
        if not updated_task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify({"id": str(updated_task.id), "status": updated_task.status.value}), 200
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid data or ID"}), 400


@tasks_blueprint.route("/tasks", methods=["GET"])
def get_tasks():
    todo_service = current_app.config['TODO_SERVICE']
    status_str = request.args.get("status")
    search_term = request.args.get("q")

    status_filter = None
    if status_str:
        try:
            status_filter = TaskStatus(status_str.lower())
        except ValueError:
            return jsonify({"error": "Invalid status"}), 400

    tasks = todo_service.list_tasks(status=status_filter, search_term=search_term)
    return jsonify([{"id": str(t.id), "title": t.title, "status": t.status.value} for t in tasks])

@tasks_blueprint.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        target_id = uuid.UUID(task_id)
        todo_service = current_app.config['TODO_SERVICE']
        todo_service.remove_task(target_id)
        return '', 204
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

@tasks_blueprint.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    # Validation
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    todo_service = current_app.config['TODO_SERVICE']
    new_task = todo_service.add_task(
        title=data["title"],
        description=data.get("description", "")
    )

    return jsonify({
        "id": str(new_task.id),
        "title": new_task.title
    }), 201

