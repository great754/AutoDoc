# registers a user, logs in to verify that the user was saved to the database.
# then it registers with a duplicate account to see if it gives the real error.
import pytest

pytestmark = pytest.mark.integration


def test_register_then_login_persists_user(client):
    register_payload = {
        "username": "integration_user",
        "full_name": "Integration User",
        "email": "integration@test.com",
        "password": "pass123",
    }

    register_response = client.post("/auth/register", json=register_payload)

    assert register_response.status_code == 200
    register_data = register_response.json()
    assert register_data["username"] == "integration_user"
    assert register_data["email"] == "integration@test.com"

    login_payload = {"username": "integration_user", "password": "pass123"}
    login_response = client.post("/auth/login", json=login_payload)

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["message"] == "Login successful"
    assert login_data["user_id"] == register_data["id"]


def test_register_duplicate_username_returns_400(client):
    payload = {
        "username": "duplicate_user",
        "full_name": "Duplicate User",
        "email": "first@test.com",
        "password": "pass123",
    }

    first_response = client.post("/auth/register", json=payload)
    assert first_response.status_code == 200

    duplicate_payload = {
        "username": "duplicate_user",
        "full_name": "Duplicate User 2",
        "email": "second@test.com",
        "password": "pass123",
    }
    duplicate_response = client.post("/auth/register", json=duplicate_payload)

    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Username already registered"
