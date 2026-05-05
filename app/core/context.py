from functools import cached_property

from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase
from redis.asyncio import Redis

from app.core.settings import Settings
from app.domain.cache_manager import CacheManagerProtocol
from app.domain.context import ContextProtocol
from app.domain.pdf_converter import PDFConverterProtocol
from app.domain.repository import RepositoryProtocol
from app.infrastructure.cache_manager import RedisCacheManager
from app.infrastructure.pdf_converter import GotenbergPDFConverter
from app.infrastructure.repository import MongoRepository
from app.infrastructure.utils import MongoDocument


class Context(ContextProtocol):
    def __init__(
        self,
        settings: Settings,
        redis_client: Redis,
        mongo_database: AsyncDatabase[MongoDocument],
        mongo_session: AsyncClientSession | None = None,
    ):
        self.settings = settings
        self.redis_client = redis_client
        self.mongo_database = mongo_database
        self.mongo_session = mongo_session

    @cached_property
    def repository(self) -> RepositoryProtocol:
        return MongoRepository(database=self.mongo_database, session=self.mongo_session)

    @cached_property
    def cache_manager(self) -> CacheManagerProtocol:
        return RedisCacheManager(client=self.redis_client)

    @cached_property
    def pdf_converter(self) -> PDFConverterProtocol:
        return GotenbergPDFConverter(host=self.settings.gotenberg_host)
