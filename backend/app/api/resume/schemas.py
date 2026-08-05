import datetime

from pydantic import BaseModel, computed_field, field_validator

from app.domain.data import MONTHS_MAP
from app.domain.resume.entities import ContactInfo, Education, Language, Project
from app.domain.skills.entities import SkillCategory


class Metadata(BaseModel):
    contact: ContactInfo
    education: list[Education]
    languages: list[Language]

    @field_validator("education", mode="after")
    @classmethod
    def sort_education(cls, value: list[Education]) -> list[Education]:
        return sorted(value, key=lambda x: x.year, reverse=True)

    @field_validator("languages", mode="after")
    @classmethod
    def sort_languages(cls, value: list[Language]) -> list[Language]:
        return sorted(value, key=lambda x: x.display_order)


class Experience(BaseModel):
    id: int
    company: str
    role: str
    context: str
    start_date: datetime.datetime
    end_date: datetime.datetime | None
    projects: list[Project]
    stack: list[str]

    @computed_field
    @property
    def period(self) -> str:
        start_date = f"{MONTHS_MAP[self.start_date.month]} {self.start_date.year}"
        end_date = (
            f"{MONTHS_MAP[self.end_date.month]} {self.end_date.year}"
            if self.end_date
            else "En cours"
        )
        return f"{start_date} - {end_date}"


class Resume(BaseModel):
    metadata: Metadata
    skills: list[SkillCategory]
    experiences: list[Experience]
