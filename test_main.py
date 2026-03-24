from database import Base, engine

# Create tables before tests
Base.metadata.create_all(bind=engine)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_students():
    response = client.get("/students")
    assert response.status_code == 200

def test_add_student():
    response = client.post("/students", json={
        "name": "Test",
        "age": 20,
        "course": "AI"
    })
    assert response.status_code == 201