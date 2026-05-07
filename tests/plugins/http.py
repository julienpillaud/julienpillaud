import datetime
import secrets
import uuid
from collections.abc import Iterator
from functools import lru_cache

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.database import Database
from pytest import FixtureRequest

from app.api.app import create_fastapi_app
from app.api.dependencies.app import get_settings
from app.core.settings import AppEnvironment, Settings
from app.domain.auth.commands import generate_access_token, generate_refresh_token
from app.domain.auth.entities import IssuedTokens
from app.domain.security import get_password_hash
from app.domain.users.entities import User
from app.infrastructure.mongo_repository.utils import MongoDocument, to_database_entity


@lru_cache
def settings_override_func() -> Settings:
    return Settings(
        environment=AppEnvironment.TESTING,
        jwt_secret=secrets.token_urlsafe(32),
        cookie_secure=False,
        access_token_expire=900,
        refresh_token_expire=604800,
        mongo_user="user",
        mongo_password="password",
        mongo_host="localhost",
        mongo_database="test",
        redis_host="localhost",
        gotenberg_host="http://localhost:3000",
    )


@pytest.fixture(scope="session")
def settings() -> Settings:
    return settings_override_func()


@pytest.fixture
def user(settings: Settings, database: Database[MongoDocument]) -> User:
    user_id = uuid.uuid7()
    user = User(
        id=user_id,
        username="user",
        hashed_password=get_password_hash("password"),
    )
    database["users"].insert_one(
        {
            "_id": user.id,
            "username": user.username,
            "hashed_password": user.hashed_password,
        }
    )
    return user


@pytest.fixture(scope="session")
def app(settings: Settings) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = settings_override_func
    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    # Use a context manager to ensure that the lifespan is called
    with TestClient(app) as client:
        yield client


@pytest.fixture
def tokens(
    request: FixtureRequest,
    settings: Settings,
    database: Database[MongoDocument],
    user: User,
    client: TestClient,
) -> IssuedTokens:
    params = getattr(request, "param", {"access": "valid", "refresh": "valid"})

    current_date = datetime.datetime.now(datetime.UTC)

    access_token = ""
    if params["access"] == "valid":
        access_token = generate_access_token(
            settings=settings,
            user_id=user.id,
            current_date=current_date,
        )
        client.cookies.set("access_token", access_token)
    elif params["access"] == "expired":
        expired_date = current_date - datetime.timedelta(days=30)
        access_token = generate_access_token(
            settings=settings,
            user_id=user.id,
            current_date=expired_date,
        )
        client.cookies.set("access_token", access_token)

    raw_refresh_token = ""
    if params["refresh"] != "none":
        raw_refresh_token = secrets.token_urlsafe(32)
        if params["refresh"] == "expired":
            token_date = current_date - datetime.timedelta(days=30)
        else:
            token_date = current_date

        refresh_token = generate_refresh_token(
            settings=settings,
            raw_value=raw_refresh_token,
            user_id=user.id,
            current_date=token_date,
        )

        if params["refresh"] == "revoked":
            refresh_token.revoked_at = current_date

        document = to_database_entity(refresh_token)
        database["refresh_tokens"].insert_one(document)
        client.cookies.set("refresh_token", raw_refresh_token)

    return IssuedTokens(
        access_token=access_token,
        refresh_token=raw_refresh_token,
        user_id=user.id,
    )
