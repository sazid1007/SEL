import pytest
from fastapi.testclient import TestClient

import app.main as task_api


@pytest.fixture(autouse=True)
def clear_tasks():
    task_api.tasks.clear()
    task_api.next_task_id = 1


@pytest.fixture
def client():
    return TestClient(task_api.app)


def task_payload():
    return {
        "title": "Write API tests",
        "description": "Cover the task lifecycle",
        "status": "todo",
        "priority": "high",
    }


def test_create_and_list_tasks(client):
    response = client.post("/tasks", json=task_payload())

    assert response.status_code == 201
    assert response.json() == {"id": 1, **task_payload()}
    assert client.get("/tasks").json() == [{"id": 1, **task_payload()}]


def test_get_task_successfully(client):
    created = client.post("/tasks", json=task_payload()).json()

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json() == created


def test_update_task_successfully(client):
    client.post("/tasks", json=task_payload())
    updated_payload = {
        "title": "Finish API tests",
        "description": "All CRUD operations are covered",
        "status": "done",
        "priority": "medium",
    }

    response = client.put("/tasks/1", json=updated_payload)

    assert response.status_code == 200
    assert response.json() == {"id": 1, **updated_payload}


def test_delete_task_successfully(client):
    client.post("/tasks", json=task_payload())

    response = client.delete("/tasks/1")

    assert response.status_code == 204
    assert client.get("/tasks/1").status_code == 404


def test_get_missing_task_returns_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_missing_task_returns_not_found(client):
    response = client.put("/tasks/999", json=task_payload())

    assert response.status_code == 404


def test_create_task_requires_title(client):
    payload = task_payload()
    del payload["title"]

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_create_task_rejects_invalid_status(client):
    payload = task_payload()
    payload["status"] = "blocked"

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
