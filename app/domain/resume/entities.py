import datetime

from pydantic import BaseModel, computed_field

from app.domain.data import MONTHS_MAP


class ContactInfo(BaseModel):
    full_name: str
    job_title: str
    email: str
    github_username: str
    linkedin_username: str
    available: bool
    location: str
    remote: str


class Education(BaseModel):
    year: int
    name: str
    school: str


class Language(BaseModel):
    display_order: int
    name: str
    level: str
    optional: bool


class SkillCategory(BaseModel):
    name: str
    display_order: int


class Skill(BaseModel):
    category: SkillCategory
    technology: str
    display_order: int


class Metadata(BaseModel):
    contact: ContactInfo
    education: list[Education]
    languages: list[Language]

    @computed_field
    @property
    def sort_languages(self) -> list[Language]:
        return sorted(self.languages, key=lambda x: x.display_order)

    @computed_field
    @property
    def sort_education(self) -> list[Education]:
        return sorted(self.education, key=lambda x: x.year, reverse=True)


class Task(BaseModel):
    label: str
    details: list[str] = []


class Project(BaseModel):
    context: str
    tasks: list[Task]


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
    skills: dict[str, list[Skill]]
    experiences: list[Experience]
