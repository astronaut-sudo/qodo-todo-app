import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, User, ToDo, get_db

# Set up test db
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Dependency override
@pytest.fixture(autouse=True)
def override_get_db(session):
    app.dependency_overrides[get_db] = lambda: session

client = TestClient(app)

# Helper for auth
def get_token(username, password):
    resp = client.post("/login", data={"username": username, "password": password})
    return resp.json()["access_token"]

def test_register_login_success():
    resp = client.post("/register", json={"username": "user", "password": "pass"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert isinstance(token, str)

    # Login
    resp = client.post("/login", data={"username": "user", "password": "pass"})
    assert resp.status_code == 200
    assert isinstance(resp.json()["access_token"], str)

def test_register_duplicate_username():
    client.post("/register", json={"username": "repeat", "password": "x"})
    resp = client.post("/register", json={"username": "repeat", "password": "y"})
    assert resp.status_code == 400
    assert "exists" in resp.json()["detail"]

def test_login_wrong_password():
    client.post("/register", json={"username": "u1", "password": "ok"})
    resp = client.post("/login", data={"username": "u1", "password": "bad"})
    assert resp.status_code == 400

def test_todo_creation_and_retrieval():
    client.post("/register", json={"username": "t", "password": "z"})
    token = get_token("t", "z")
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/todos", headers=headers, json={"content": "do thing", "priority": "high", "status": "not_started"})
    assert resp.status_code == 200
    assert resp.json()["content"] == "do thing"

    resp = client.get("/todos", headers=headers)
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["content"] == "do thing"
    assert data[0]["priority"] == "high"
    assert data[0]["status"] == "not_started"

    # Test filter for completed
    resp = client.get("/todos?completed=true", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == []  # none completed yet

def test_empty_content_invalid_priority_status():
    client.post("/register", json={"username": "v", "password": "k"})
    token = get_token("v", "k")
    headers = {"Authorization": f"Bearer {token}"}

    # Empty content
    resp = client.post("/todos", headers=headers, json={"content": "", "priority": "high", "status": "not_started"})
    assert resp.status_code in (422, 400)
    # Bad priority
    resp = client.post("/todos", headers=headers, json={"content": "task", "priority": "unknown", "status": "not_started"})
    assert resp.status_code in (422, 400)
    # Bad status
    resp = client.post("/todos", headers=headers, json={"content": "task", "priority": "high", "status": "unknown"})
    assert resp.status_code in (422, 400)

def test_unauthorized_access():
    resp = client.get("/todos")
    assert resp.status_code == 401
    resp = client.post("/todos", json={"content": "bad", "priority": "low", "status": "not_started"})
    assert resp.status_code == 401

def test_delete_and_update():
    client.post("/register", json={"username": "deluser", "password": "q"})
    token = get_token("deluser", "q")
    headers = {"Authorization": f"Bearer {token}"}
    todo = client.post("/todos", headers=headers, json={"content": "ok", "priority": "medium", "status": "in_progress"}).json()
    id = todo["id"]

    resp = client.patch(f"/todos/{id}", headers=headers, json={"status": "completed"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"
    resp = client.delete(f"/todos/{id}", headers=headers)
    assert resp.status_code == 200
    # Now gone
    resp = client.get("/todos", headers=headers)
    assert all(t["id"] != id for t in resp.json())
