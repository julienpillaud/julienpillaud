import secrets
import uuid
from collections.abc import Iterator
from functools import lru_cache

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.database import Database

from app.api.app import create_fastapi_app
from app.api.dependencies.app import get_settings
from app.api.security import generate_tokens
from app.core.settings import AppEnvironment, Settings
from app.domain.admin.entities import User
from app.domain.security import get_password_hash
from app.infrastructure.repository import MongoDocument


@lru_cache
def settings_override_func() -> Settings:
    return Settings(
        environment=AppEnvironment.TESTING,
        jwt_secret=secrets.token_urlsafe(32),
        access_token_expire=900,
        refresh_token_expire=604800,
        mongo_user="user",
        mongo_password="password",
        mongo_host="localhost",
        mongo_database="test",
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
def logged_user(settings: Settings, user: User, client: TestClient) -> User:
    access_token, refresh_token = generate_tokens(
        settings=settings,
        user_id=user.id,
    )

    client.cookies.set("access_token", access_token)
    client.cookies.set("refresh_token", refresh_token.value)

    return user
