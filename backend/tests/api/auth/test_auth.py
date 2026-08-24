import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.auth.entities import IssuedTokens


@pytest.mark.parametrize(
    "tokens",
    [{"access": "valid", "refresh": "none"}],
    indirect=True,
)
def test_get_me(client: TestClient, tokens: IssuedTokens) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == status.HTTP_200_OK


def test_get_me_no_token(client: TestClient) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    result = response.json()
    assert result["detail"] == "No valid token found"


@pytest.mark.parametrize(
    "tokens",
    [{"access": "expired", "refresh": "none"}],
    indirect=True,
)
def test_get_me_expired_token(client: TestClient, tokens: IssuedTokens) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    result = response.json()
    assert result["detail"] == "Token expired"
