from enum import StrEnum
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

app_path = Path(__file__).resolve().parents[1]


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", frozen=True, env_file=".env")

    environment: AppEnvironment
    logfire_token: str = ""
    template_path: Path = app_path / "templates"

    full_name: str
    job_title: str
    email: str
    github: str
    linkedin: str

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_database: str

    @computed_field
    @property
    def mongo_uri(self) -> str:
        pattern = "mongodb+srv://{user}:{password}@{host}"
        return pattern.format(
            user=self.mongo_user,
            password=self.mongo_password,
            host=self.mongo_host,
        )
