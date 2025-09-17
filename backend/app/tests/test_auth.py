import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


def test_login(client: TestClient, test_user):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, test_user):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password"
        }
    )
    assert response.status_code == 401


def test_register(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "newpassword",
            "full_name": "New User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"


def test_register_existing_email(client: TestClient, test_user):
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "email": test_user.email,
            "password": "password",
            "full_name": "Another User"
        }
    )
    assert response.status_code == 400