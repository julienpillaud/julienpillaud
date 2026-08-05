import datetime

from pydantic import BaseModel

from app.domain.skills.entities import SkillCategory


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


class Metadata(BaseModel):
    contact: ContactInfo
    education: list[Education]
    languages: list[Language]


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


class Resume(BaseModel):
    metadata: Metadata
    skills: list[SkillCategory]
    experiences: list[Experience]
