from app.domain.repository import RepositoryProtocol
from app.domain.resume.entities import Resume
from app.domain.skills.commands import get_skills_command


async def get_resume_command(repository: RepositoryProtocol, /) -> Resume:
    metadata = await repository.get_metadata()
    experiences = await repository.get_experiences()
    skills = await get_skills_command(repository)
    return Resume(
        metadata=metadata,
        skills=skills,
        experiences=experiences,
    )
