import pytest

pytestmark = pytest.mark.unit


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_success(client):
    payload = {
        "username": "great754",
        "full_name": "Great Abhieyighan",
        "email": "great@test.com",
        "password": "secret",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "great754"
    assert data["email"] == "great@test.com"
    assert "id" in data
    assert "password" not in data


def test_login_success(client):

    # setup
    register_payload = {
        "username": "great754",
        "full_name": "Great Abhieyighan",
        "email": "great@test.com",
        "password": "pass123",
    }
    client.post("/auth/register", json=register_payload)

    # action
    login_payload = {"username": "great754", "password": "pass123"}
    response = client.post("/auth/login", json=login_payload)

    # assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert "user_id" in data


def test_invalid_login(client):
    login_payload = {"username": "fakelogin", "password": "test"}
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid username or password"
