import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pymongo.synchronous.database import Database

from app.domain.auth.entities import IssuedTokens
from app.domain.users.entities import User
from app.infrastructure.mongo_repository.utils import MongoDocument


@pytest.mark.parametrize(
    "tokens",
    [{"access": "valid", "refresh": "valid"}],
    indirect=True,
)
def test_logout_no_redirect(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
    database: Database[MongoDocument],
) -> None:
    response = client.post("/auth/logout", follow_redirects=False)

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/auth"
    cookies = response.headers["set-cookie"]
    assert 'access_token=""' in cookies
    assert 'refresh_token=""' in cookies

    refresh_tokens = database["refresh_tokens"].find({"user_id": user.id}).to_list()
    assert len(refresh_tokens) == 1
    assert refresh_tokens[0]["revoked_at"] is not None


def test_logout_unknown_user(client: TestClient) -> None:
    response = client.post("/auth/logout")

    # raise AuthorizationError
    # response made by auth_exception_handler
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "error.html"  # type: ignore[attr-defined, ty:unresolved-attribute]
