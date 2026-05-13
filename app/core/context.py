from functools import cached_property

from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase
from redis.asyncio import Redis

from app.core.settings import Settings
from app.domain.auth.repository import RefreshTokenRepositoryProtocol
from app.domain.cache_manager import CacheManagerProtocol
from app.domain.context import ContextProtocol
from app.domain.pdf_converter import PDFConverterProtocol
from app.domain.repository import RepositoryProtocol
from app.domain.skills.repository import SkillRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.cache_manager import RedisCacheManager
from app.infrastructure.mongo_repository.refresh_tokens import RefreshTokenRepository
from app.infrastructure.mongo_repository.skills import SkillRepository
from app.infrastructure.mongo_repository.users import UserRepository
from app.infrastructure.mongo_repository.utils import MongoDocument
from app.infrastructure.pdf_converter import GotenbergPDFConverter
from app.infrastructure.repository import MongoRepository


class Context(ContextProtocol):
    def __init__(
        self,
        settings: Settings,
        redis_client: Redis,
        mongo_database: AsyncDatabase[MongoDocument],
        mongo_session: AsyncClientSession | None = None,
    ) -> None:
        self.settings = settings
        self.redis_client = redis_client
        self.mongo_database = mongo_database
        self.mongo_session = mongo_session

    @cached_property
    def repository(self) -> RepositoryProtocol:
        return MongoRepository(
            database=self.mongo_database,
            session=self.mongo_session,
        )

    @cached_property
    def refresh_token_repository(self) -> RefreshTokenRepositoryProtocol:
        return RefreshTokenRepository(
            database=self.mongo_database,
            session=self.mongo_session,
        )

    @cached_property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserRepository(
            database=self.mongo_database,
            session=self.mongo_session,
        )

    @cached_property
    def skill_repository(self) -> SkillRepositoryProtocol:
        return SkillRepository(
            database=self.mongo_database,
            session=self.mongo_session,
        )

    @cached_property
    def cache_manager(self) -> CacheManagerProtocol:
        return RedisCacheManager(client=self.redis_client)

    @cached_property
    def pdf_converter(self) -> PDFConverterProtocol:
        return GotenbergPDFConverter(host=self.settings.gotenberg_host)
