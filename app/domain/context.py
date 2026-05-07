from typing import Protocol

from app.domain.auth.repository import RefreshTokenRepositoryProtocol
from app.domain.cache_manager import CacheManagerProtocol
from app.domain.pdf_converter import PDFConverterProtocol
from app.domain.repository import RepositoryProtocol
from app.domain.skills.repository import SkillRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def repository(self) -> RepositoryProtocol: ...

    @property
    def refresh_token_repository(self) -> RefreshTokenRepositoryProtocol: ...

    @property
    def user_repository(self) -> UserRepositoryProtocol: ...

    @property
    def skill_repository(self) -> SkillRepositoryProtocol: ...

    @property
    def cache_manager(self) -> CacheManagerProtocol: ...

    @property
    def pdf_converter(self) -> PDFConverterProtocol: ...
