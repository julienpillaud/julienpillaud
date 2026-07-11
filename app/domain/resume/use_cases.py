from app.domain.context import ContextProtocol
from app.domain.resume.entities import Resume
from app.domain.skills.use_cases.skills import get_skill_categories


async def get_resume(context: ContextProtocol, /) -> Resume:
    metadata = await context.repository.get_metadata()
    experiences = await context.repository.get_experiences()
    skills = await get_skill_categories(context)
    return Resume(
        metadata=metadata,
        skills=skills,
        experiences=experiences,
    )
