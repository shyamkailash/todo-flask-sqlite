from flask import Flask, request, jsonify
from flask_cors import CORS

from database import (
    create_table,
    add_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task
)


app = Flask(__name__)
CORS(app)

create_table()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "To-Do Flask SQLite API is running"
    })


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Backend is healthy"
    })


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = get_all_tasks()

    return jsonify({
        "status": "success",
        "count": len(tasks),
        "tasks": tasks
    })


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_single_task(task_id):
    task = get_task_by_id(task_id)

    if task is None:
        return jsonify({
            "status": "error",
            "message": "Task not found"
        }), 404

    return jsonify({
        "status": "success",
        "task": task
    })


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({
            "status": "error",
            "message": "Task is required"
        }), 400

    task_text = data["task"].strip()

    if task_text == "":
        return jsonify({
            "status": "error",
            "message": "Task cannot be empty"
        }), 400

    task_id = add_task(task_text)
    new_task = get_task_by_id(task_id)

    return jsonify({
        "status": "success",
        "message": "Task added successfully",
        "task": new_task
    }), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    task = get_task_by_id(task_id)

    if task is None:
        return jsonify({
            "status": "error",
            "message": "Task not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data provided"
        }), 400

    task_text = data.get("task")
    status = data.get("status")

    if status and status not in ["Pending", "Completed"]:
        return jsonify({
            "status": "error",
            "message": "Status must be Pending or Completed"
        }), 400

    if task_text is not None:
        task_text = task_text.strip()

        if task_text == "":
            return jsonify({
                "status": "error",
                "message": "Task cannot be empty"
            }), 400

    update_task(task_id, task_text, status)
    updated_task = get_task_by_id(task_id)

    return jsonify({
        "status": "success",
        "message": "Task updated successfully",
        "task": updated_task
    })


@app.route("/api/tasks/<int:task_id>/complete", methods=["PUT"])
def mark_task_completed(task_id):
    task = get_task_by_id(task_id)

    if task is None:
        return jsonify({
            "status": "error",
            "message": "Task not found"
        }), 404

    update_task(task_id, status="Completed")
    updated_task = get_task_by_id(task_id)

    return jsonify({
        "status": "success",
        "message": "Task marked as completed",
        "task": updated_task
    })


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    task = get_task_by_id(task_id)

    if task is None:
        return jsonify({
            "status": "error",
            "message": "Task not found"
        }), 404

    delete_task(task_id)

    return jsonify({
        "status": "success",
        "message": "Task deleted successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)