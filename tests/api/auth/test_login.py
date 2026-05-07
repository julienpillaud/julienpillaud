import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pymongo.synchronous.database import Database

from app.domain.auth.entities import IssuedTokens
from app.domain.users.entities import User
from app.infrastructure.mongo_repository.utils import MongoDocument


def test_get_login(client: TestClient) -> None:
    # When we get /auth
    response = client.get("/auth")

    # Then we get the login page
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "login.html"  # type: ignore[attr-defined]
    assert response.context["error"] is None  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "tokens",
    [{"access": "valid", "refresh": "valid"}],
    indirect=True,
)
def test_get_login_authenticated(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
) -> None:
    # Given an authenticated user
    # When we get /auth
    response = client.get("/auth")

    # Then we are redirected to the admin page
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "admin.html"  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "tokens",
    [{"access": "none", "refresh": "none"}],
    indirect=True,
)
def test_post_login_invalid_credentials(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
) -> None:
    # Given an existing user
    # When we post /auth with bad password
    response = client.post("/auth", data={"username": user.username, "password": "bad"})

    # Then we stay in login page with error message
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "login.html"  # type: ignore[attr-defined]
    assert response.context["error"] == "Invalid credentials"  # type: ignore[attr-defined]


def test_post_login_unknown_user(client: TestClient) -> None:
    # Given NO existing user
    # When we post /auth
    response = client.post("/auth", data={"username": "user", "password": "password"})

    # Then we stay in login page with error message
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "login.html"  # type: ignore[attr-defined]
    assert response.context["error"] == "Invalid credentials"  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "tokens",
    [{"access": "none", "refresh": "none"}],
    indirect=True,
)
def test_post_login_valid_credentials_no_redirect(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
) -> None:
    # Given an existing user
    # When we post /auth (without following redirect)
    response = client.post(
        "/auth",
        data={"username": user.username, "password": "password"},
        follow_redirects=False,
    )

    # Then the tokens are set in the response
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.parametrize(
    "tokens",
    [{"access": "none", "refresh": "none"}],
    indirect=True,
)
def test_post_login_valid_credentials(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
    database: Database[MongoDocument],
) -> None:
    # Given an existing user
    # When we post /auth
    response = client.post(
        "/auth",
        data={"username": user.username, "password": "password"},
    )

    # Then we are redirected to the admin page
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "admin.html"  # type: ignore[attr-defined]

    refresh_tokens = database["refresh_tokens"].find({"user_id": user.id}).to_list()
    assert len(refresh_tokens) == 1
    assert refresh_tokens[0]["revoked_at"] is None
