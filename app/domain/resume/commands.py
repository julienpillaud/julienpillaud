from app.domain.repository import RepositoryProtocol
from app.domain.resume.entities import Resume
from app.domain.skills.commands.skills import get_skill_categories_command


async def get_resume_command(repository: RepositoryProtocol, /) -> Resume:
    metadata = await repository.get_metadata()
    experiences = await repository.get_experiences()
    skills = await get_skill_categories_command(repository)
    return Resume(
        metadata=metadata,
        skills=skills,
        experiences=experiences,
    )
