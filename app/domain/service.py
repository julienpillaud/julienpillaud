from app.core.settings import Settings
from app.domain.entities import Metadata, Resume
from app.domain.repository import RepositoryProtocol


async def get_resume(settings: Settings, repository: RepositoryProtocol) -> Resume:
    experiences = await repository.get_experiences()
    resume = Resume(
        full_name=settings.full_name,
        job_title=settings.job_title,
        email=settings.email,
        github=settings.github,
        linkedin=settings.linkedin,
        metadata=Metadata(
            skills=[],
            education=[],
            languages=[],
        ),
        experiences=experiences,
    )
    return resume
