from collections.abc import Callable
from functools import cached_property

from pymongo.asynchronous.client_session import AsyncClientSession
from redis.asyncio import Redis

from app.core.domain import TransactionProtocol
from app.core.settings import Settings
from app.domain.auth.repository import RefreshTokenRepositoryProtocol
from app.domain.cache_manager import CacheManagerProtocol
from app.domain.context import ContextProtocol
from app.domain.repository import RepositoryProtocol
from app.domain.skills.repository import SkillRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.cache_manager import RedisCacheManager
from app.infrastructure.mongo_repository.refresh_tokens import RefreshTokenRepository
from app.infrastructure.mongo_repository.resource.asynchronous import MongoTransaction
from app.infrastructure.mongo_repository.skills import SkillRepository
from app.infrastructure.mongo_repository.users import UserRepository
from app.infrastructure.repository import MongoRepository

type ContextFactory = Callable[[AsyncClientSession | None], ContextProtocol]


class Context(ContextProtocol):
    def __init__(
        self,
        settings: Settings,
        redis_client: Redis,
        transaction: MongoTransaction,
    ) -> None:
        self.settings = settings
        self.redis_client = redis_client
        self.database = transaction.resource.database
        self.session = transaction.session

    @cached_property
    def repository(self) -> RepositoryProtocol:
        return MongoRepository(database=self.database, session=self.session)

    @cached_property
    def refresh_token_repository(self) -> RefreshTokenRepositoryProtocol:
        return RefreshTokenRepository(database=self.database, session=self.session)

    @cached_property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserRepository(database=self.database, session=self.session)

    @cached_property
    def skill_repository(self) -> SkillRepositoryProtocol:
        return SkillRepository(database=self.database, session=self.session)

    @cached_property
    def cache_manager(self) -> CacheManagerProtocol:
        return RedisCacheManager(client=self.redis_client)


class ContextProvider:
    def __init__(
        self,
        settings: Settings,
        redis_client: Redis,
    ) -> None:
        self._settings = settings
        self._redis_client = redis_client

    def __call__(self, transaction: TransactionProtocol) -> Context:
        if not isinstance(transaction, MongoTransaction):
            raise RuntimeError()

        return Context(
            settings=self._settings,
            redis_client=self._redis_client,
            transaction=transaction,
        )
