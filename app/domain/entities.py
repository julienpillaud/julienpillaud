from enum import StrEnum

from pydantic import BaseModel


class ContactInfo(BaseModel):
    full_name: str
    job_title: str
    email: str
    github_username: str
    linkedin_username: str
    available: bool
    location: str
    remote: str


class SkillCategory(StrEnum):
    DEVELOPMENT = "Développement"
    TESTING_QUALITY = "Tests & Qualité"
    DATABASE = "Bases de données"
    INFRA = "CI/CD - Cloud"


class Skill(BaseModel):
    order: int
    category: SkillCategory
    technology: str


class Metadata(BaseModel):
    contact: ContactInfo
    education: list[str]
    languages: list[str]


class Task(BaseModel):
    label: str
    details: list[str] = []


class Project(BaseModel):
    context: str
    tasks: list[Task]
    stack: list[str] = []


class Experience(BaseModel):
    id: int
    company: str
    role: str
    start_date: str
    end_date: str | None = None
    projects: list[Project]


class Resume(BaseModel):
    metadata: Metadata
    skills: dict[SkillCategory, list[Skill]]
    experiences: list[Experience]
