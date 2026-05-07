import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pymongo.synchronous.database import Database

from app.domain.auth.entities import IssuedTokens
from app.domain.users.entities import User
from app.infrastructure.mongo_repository.utils import MongoDocument


@pytest.mark.parametrize(
    "tokens",
    [{"access": "none", "refresh": "valid"}],
    indirect=True,
)
def test_auth_refresh_only(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
    database: Database[MongoDocument],
) -> None:
    response = client.get("/admin")

    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "admin.html"  # type: ignore[attr-defined]

    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies

    all_tokens = database["refresh_tokens"].find({"user_id": user.id}).to_list()

    revoked = [t for t in all_tokens if t["revoked_at"] is not None]
    active = [t for t in all_tokens if t["revoked_at"] is None]

    assert len(revoked) == 1
    assert len(active) == 1


@pytest.mark.parametrize(
    "tokens",
    [{"access": "none", "refresh": "expired"}],
    indirect=True,
)
def test_auth_refresh_expired(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
    database: Database[MongoDocument],
) -> None:
    response = client.get("/admin")

    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "error.html"  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "tokens",
    [{"access": "none", "refresh": "revoked"}],
    indirect=True,
)
def test_auth_refresh_revoked(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
    database: Database[MongoDocument],
) -> None:
    response = client.get("/admin")

    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "error.html"  # type: ignore[attr-defined]
