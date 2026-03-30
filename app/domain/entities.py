from pydantic import BaseModel, EmailStr, HttpUrl


class Skill(BaseModel):
    category: str
    technologies: list[str]


class Metadata(BaseModel):
    skills: list[Skill]
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
    full_name: str
    job_title: str
    email: EmailStr
    github: HttpUrl | None = None
    linkedin: HttpUrl | None = None
    metadata: Metadata
    experiences: list[Experience]
