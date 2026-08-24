import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.auth.entities import IssuedTokens
from app.domain.users.entities import User


@pytest.mark.parametrize(
    "tokens",
    [{"access": "valid", "refresh": "none"}],
    indirect=True,
)
def test_logout(
    client: TestClient,
    user: User,
    tokens: IssuedTokens,
) -> None:
    response = client.post("/api/auth/logout")

    assert response.status_code == status.HTTP_200_OK


def test_logout_unauthorized(client: TestClient) -> None:
    response = client.post("/api/auth/logout")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    result = response.json()
    assert result["detail"] == "No valid token found"
