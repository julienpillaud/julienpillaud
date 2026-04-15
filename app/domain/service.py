from collections import defaultdict

from app.domain.entities import Resume, Skill
from app.domain.repository import RepositoryProtocol


async def get_skills(repository: RepositoryProtocol) -> dict[str, list[Skill]]:
    raw_skills = await repository.get_skills()

    skills = defaultdict(list)
    for skill in raw_skills:
        skills[skill.category.name].append(skill)

    return dict(skills)


async def get_resume(repository: RepositoryProtocol) -> Resume:
    metadata = await repository.get_metadata()
    experiences = await repository.get_experiences()
    skills = await get_skills(repository=repository)
    return Resume(
        metadata=metadata,
        skills=skills,
        experiences=experiences,
    )
