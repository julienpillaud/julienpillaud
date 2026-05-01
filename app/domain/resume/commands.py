from app.domain.context import ContextProtocol
from app.domain.resume.entities import Resume
from app.domain.skills.commands.skills import get_skill_categories_command


async def get_resume_command(context: ContextProtocol, /) -> Resume:
    metadata = await context.repository.get_metadata()
    experiences = await context.repository.get_experiences()
    skills = await get_skill_categories_command(context)
    return Resume(
        metadata=metadata,
        skills=skills,
        experiences=experiences,
    )
