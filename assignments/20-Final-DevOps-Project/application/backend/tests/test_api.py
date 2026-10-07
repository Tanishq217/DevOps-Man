import os
import pytest
from fastapi.testclient import TestClient

# Use an isolated in-memory or SQLite database for tests
os.environ["DATABASE_URL"] = "sqlite:///./test_taskboard.db"

from app.main import app
from app.db import engine, Base
from app import models  # noqa: F401


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_taskboard.db"):
        os.remove("./test_taskboard.db")


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert "service" in data


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert "endpoints" in data


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"
    assert data["database"] == "CONNECTED"


def test_create_task(client):
    payload = {
        "title": "Configure Prometheus Alerts",
        "description": "Write alert rules for HighErrorRate and PodCrashLooping",
        "priority": "HIGH",
        "status": "TODO",
        "assignee": "Tanishq Singh",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["priority"] == "HIGH"
    assert "id" in created


def test_create_task_validation_error(client):
    # Empty title should trigger Pydantic 422 error
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) > 0


def test_filter_tasks_by_status(client):
    response = client.get("/api/tasks?status=TODO")
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["status"] == "TODO" for t in tasks)


def test_get_task_by_id(client):
    # First create a task
    create_res = client.post(
        "/api/tasks",
        json={"title": "Unique Task For Lookup", "status": "IN_PROGRESS"},
    )
    task_id = create_res.json()["id"]

    # Now get it
    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Unique Task For Lookup"


def test_get_task_not_found(client):
    response = client.get("/api/tasks/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_task(client):
    create_res = client.post(
        "/api/tasks",
        json={"title": "Task To Update", "status": "TODO", "priority": "LOW"},
    )
    task_id = create_res.json()["id"]

    update_res = client.put(
        f"/api/tasks/{task_id}",
        json={"status": "DONE", "priority": "HIGH"},
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["status"] == "DONE"
    assert updated["priority"] == "HIGH"


def test_update_task_not_found(client):
    response = client.put("/api/tasks/999999", json={"title": "Non-existent"})
    assert response.status_code == 404


def test_delete_task(client):
    create_res = client.post(
        "/api/tasks",
        json={"title": "Task To Delete"},
    )
    task_id = create_res.json()["id"]

    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == 204

    # Verify deleted
    verify_res = client.get(f"/api/tasks/{task_id}")
    assert verify_res.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/api/tasks/999999")
    assert response.status_code == 404


def test_stats_aggregation(client):
    response = client.get("/api/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total" in stats
    assert "todo" in stats
    assert "inProgress" in stats
    assert "done" in stats
    assert stats["total"] >= stats["todo"] + stats["inProgress"] + stats["done"]


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests" in response.text or "python_info" in response.text or "process_cpu" in response.text
