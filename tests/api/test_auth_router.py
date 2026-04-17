from fastapi import status
from fastapi.testclient import TestClient

from app.domain.admin.entities import User


def test_get_login(client: TestClient) -> None:
    response = client.get("/auth")

    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "login.html"  # type: ignore[attr-defined]
    assert response.context["error"] is None  # type: ignore[attr-defined]


def test_get_login_authenticated(client: TestClient, logged_user: User) -> None:
    response = client.get("/auth")

    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "admin.html"  # type: ignore[attr-defined]


def test_post_login_invalid_credentials(client: TestClient) -> None:
    response = client.post("/auth", data={"username": "user", "password": "bad"})

    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "login.html"  # type: ignore[attr-defined]
    assert response.context["error"] == "Invalid credentials"  # type: ignore[attr-defined]


def test_post_login_valid_credentials(client: TestClient, logged_user: User) -> None:
    response = client.post(
        "/auth",
        data={"username": logged_user.username, "password": "password"},
        follow_redirects=False,
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_post_login_valid_credentials_redirect(
    client: TestClient,
    logged_user: User,
) -> None:
    response = client.post(
        "/auth",
        data={"username": logged_user.username, "password": "password"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "admin.html"  # type: ignore[attr-defined]


def test_logout(client: TestClient, logged_user: User) -> None:
    response = client.post("/auth/logout", follow_redirects=False)

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies


def test_logout_unauthenticated(client: TestClient) -> None:
    response = client.post("/auth/logout")

    # raise AuthorizationError
    # response made by auth_exception_handler
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "error.html"  # type: ignore[attr-defined]
