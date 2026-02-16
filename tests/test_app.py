import pytest
from src.app import create_app
import os


@pytest.fixture
def client():
    test_db = "test_web_tasks.csv"
    app = create_app(storage_path=test_db)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    if os.path.exists(test_db):
        os.remove(test_db)


def test_filter_tasks_by_status(client):
    client.post("/tasks", json={"title": "Pending Task"})
    done_task = client.post("/tasks", json={"title": "Done Task"})
    client.patch(f"/tasks/{done_task.json['id']}", json={"status": "done"})

    response = client.get("/tasks?status=done")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Done Task"

def test_toggle_task_status(client):
    create_res = client.post("/tasks", json={"title": "Toggle Me"})
    task_id = create_res.json["id"]

    patch_res = client.patch(f"/tasks/{task_id}", json={
        "status": "done"
    })

    # Assert
    assert patch_res.status_code == 200
    assert patch_res.json["status"] == "done"

def test_get_tasks_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json == []


def test_create_task_via_api(client):
    response = client.post("/tasks", json={
        "title": "Postman Task",
        "description": "Created via API"
    })

    assert response.status_code == 201
    assert response.json["title"] == "Postman Task"
    assert "id" in response.json


def test_delete_task_via_api(client):
    create_res = client.post("/tasks", json={"title": "Delete Me"})
    task_id = create_res.json["id"]

    delete_res = client.delete(f"/tasks/{task_id}")

    assert delete_res.status_code == 204
    get_res = client.get("/tasks")
    assert not any(t["id"] == task_id for t in get_res.json)