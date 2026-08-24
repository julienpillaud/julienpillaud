from fastapi import status
from fastapi.testclient import TestClient

from app.domain.users.entities import User


def test_login(user: User, client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        data={"username": user.username, "password": "password"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_login_unknown_user(client: TestClient, user: User) -> None:
    response = client.post(
        "/api/auth/login",
        data={"username": "unknown", "password": "password"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    result = response.json()
    assert result["detail"] == "Invalid credentials"


def test_login_bad_credentials(user: User, client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        data={"username": user.username, "password": "bad"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    result = response.json()
    assert result["detail"] == "Invalid credentials"
