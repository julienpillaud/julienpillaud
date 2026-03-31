from collections import defaultdict

from app.domain.entities import Resume
from app.domain.repository import RepositoryProtocol


async def get_resume(repository: RepositoryProtocol) -> Resume:
    metadata = await repository.get_metadata()

    experiences = await repository.get_experiences()

    raw_skills = await repository.get_skills()
    skills = defaultdict(list)
    for skill in raw_skills:
        skills[skill.category].append(skill)

    return Resume(
        metadata=metadata,
        skills=dict(skills),
        experiences=experiences,
    )
