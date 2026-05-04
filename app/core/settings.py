from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_PATH = Path(__file__).resolve().parents[1]


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class AppPaths(BaseModel):
    model_config = ConfigDict(frozen=True)

    app_path: Path = APP_PATH
    templates: Path = APP_PATH / "templates"
    static: Path = APP_PATH / "static"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", frozen=True, env_file=".env")

    environment: AppEnvironment
    logfire_token: str = ""
    paths: AppPaths = AppPaths()

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire: int
    refresh_token_expire: int

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_database: str

    redis_host: str
    redis_port: int = 6379

    gotenberg_host: str

    @computed_field
    @property
    def mongo_uri(self) -> str:
        if self.environment == AppEnvironment.TESTING:
            return "mongodb://localhost:27017?replicaSet=rs0"

        pattern = "mongodb+srv://{user}:{password}@{host}"
        return pattern.format(
            user=self.mongo_user,
            password=self.mongo_password,
            host=self.mongo_host,
        )

    @computed_field
    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            path="0",
        )
