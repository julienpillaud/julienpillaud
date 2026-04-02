from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, computed_field
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
    api_key: str

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_database: str

    gotenberg_host: str

    @computed_field
    @property
    def mongo_uri(self) -> str:
        pattern = "mongodb+srv://{user}:{password}@{host}"
        return pattern.format(
            user=self.mongo_user,
            password=self.mongo_password,
            host=self.mongo_host,
        )
