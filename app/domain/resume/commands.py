from collections import defaultdict

from app.domain.repository import RepositoryProtocol
from app.domain.resume.entities import Resume, Skill


async def get_raw_skills(repository: RepositoryProtocol, /) -> list[Skill]:
    return await repository.get_skills()


async def get_skills(repository: RepositoryProtocol, /) -> dict[str, list[Skill]]:
    raw_skills = await repository.get_skills()

    skills = defaultdict(list)
    for skill in raw_skills:
        skills[skill.category.name].append(skill)

    return dict(skills)


async def get_resume(repository: RepositoryProtocol, /) -> Resume:
    metadata = await repository.get_metadata()
    experiences = await repository.get_experiences()
    skills = await get_skills(repository)
    return Resume(
        metadata=metadata,
        skills=skills,
        experiences=experiences,
    )
