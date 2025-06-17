from datetime import date, timedelta

from tests.conftest import client


def test_create_task():
    payload = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": str(date.today() + timedelta(days=3)),
        "status": "pending",
    }

    response = client.post("/tasks", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["due_date"] == payload["due_date"]
    assert data["status"] == payload["status"]


def test_get_all_tasks():
    client.post("/tasks", json={"title": "Task 1", "status": "pending"})
    client.post("/tasks", json={"title": "Task 2", "status": "completed"})

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()

    titles = [task["title"] for task in tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles


def test_get_tasks_filtered_by_status():
    client.post("/tasks", json={"title": "Task 1", "status": "pending"})
    client.post("/tasks", json={"title": "Task 2", "status": "completed"})
    client.post("/tasks", json={"title": "Task 3", "status": "completed"})

    response = client.get("/tasks", params={"status": "completed"})
    assert response.status_code == 200
    completed_tasks = response.json()

    assert len(completed_tasks) == 2
    for task in completed_tasks:
        assert task["status"] == "completed"


def test_update_task():
    create_resp = client.post("/tasks", json={"title": "Old Task"})
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    update_payload = {
        "title": "Updated Task",
        "description": "Updated Description",
        "status": "in-progress",
        "due_date": str(date.today() + timedelta(days=5)),
    }
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == update_payload["title"]
    assert data["description"] == update_payload["description"]
    assert data["status"] == update_payload["status"]
    assert data["due_date"] == update_payload["due_date"]
    assert data["id"] == task_id


def test_delete_task():
    create_resp = client.post("/tasks", json={"title": "Delete Me"})
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    tasks = client.get("/tasks").json()
    assert all(task["id"] != task_id for task in tasks)


def test_update_nonexistent_task():
    update_payload = {
        "title": "Nonexistent Task",
        "description": "Should fail",
        "status": "pending",
    }
    response = client.put("/tasks/99999", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id 99999 not found"


def test_delete_nonexistent_task():
    response = client.delete("/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id 99999 not found"
