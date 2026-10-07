import pytest
import json
import sys
import os

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"DevSecOps Automated Delivery Dashboard" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data


def test_status(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"
    assert "platform" in data
    assert "python_version" in data
    assert "total_requests" in data


def test_greet(client):
    response = client.get("/api/greet/Tanishq")
    assert response.status_code == 200
    data = response.get_json()
    assert "Tanishq" in data["message"]


def test_add_numbers_success(client):
    response = client.post(
        "/api/add",
        data=json.dumps({"number1": 15, "number2": 25}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 40


def test_add_numbers_missing_fields(client):
    response = client.post(
        "/api/add",
        data=json.dumps({"number1": 10}),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_calculate_add(client):
    response = client.post(
        "/api/calculate",
        data=json.dumps({"a": 12, "b": 8, "operation": "add"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == 20


def test_calculate_subtract(client):
    response = client.post(
        "/api/calculate",
        data=json.dumps({"a": 20, "b": 5, "operation": "-"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == 15


def test_calculate_multiply(client):
    response = client.post(
        "/api/calculate",
        data=json.dumps({"a": 7, "b": 6, "operation": "multiply"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == 42


def test_calculate_divide(client):
    response = client.post(
        "/api/calculate",
        data=json.dumps({"a": 50, "b": 2, "operation": "divide"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == 25.0


def test_calculate_divide_by_zero(client):
    response = client.post(
        "/api/calculate",
        data=json.dumps({"a": 10, "b": 0, "operation": "divide"}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert "Division by zero" in response.get_json()["error"]


def test_calculate_unsupported_operation(client):
    response = client.post(
        "/api/calculate",
        data=json.dumps({"a": 10, "b": 2, "operation": "exponent"}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert "Unsupported arithmetic operation" in response.get_json()["error"]
