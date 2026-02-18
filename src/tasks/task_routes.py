import uuid
from flask import Blueprint, jsonify, request, current_app

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": str(e)}), 400

@tasks_bp.errorhandler(RuntimeError)
def handle_runtime_error(e):
    return jsonify({"error": "A server error occurred"}), 500

@tasks_bp.route("/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    todo_service = current_app.config['TASK_SERVICE']
    data = request.get_json()

    target_id = uuid.UUID(task_id)
    updated_task = todo_service.update_task(target_id, **data)
    if not updated_task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"id": str(updated_task.id), "status": updated_task.status.value}), 200

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    print(1)
    todo_service = current_app.config['TASK_SERVICE']
    print(2, todo_service)
    status_str = request.args.get("status")
    print(3, status_str)
    search_term = request.args.get("q")
    print(4, search_term)

    tasks = todo_service.list_tasks(status=status_str, search_term=search_term)
    print(5, tasks)

    return jsonify([{"id": str(t.id), "title": t.title, "status": t.status.value} for t in tasks])

@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    target_id = uuid.UUID(task_id)
    todo_service = current_app.config['TASK_SERVICE']
    result = todo_service.remove_task(target_id)
    if result:
        return '', 204
    return jsonify({"error": "Task not found"}), 404


@tasks_bp.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    # Validation
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    todo_service = current_app.config['TASK_SERVICE']
    new_task = todo_service.add_task(
        title=data["title"],
        description=data.get("description", "")
    )

    return jsonify({
        "id": str(new_task.id),
        "title": new_task.title
    }), 201

