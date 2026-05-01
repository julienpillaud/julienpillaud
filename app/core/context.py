from functools import cached_property

from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from app.core.settings import Settings
from app.domain.context import ContextProtocol
from app.domain.pdf_converter import PDFConverterProtocol
from app.domain.repository import RepositoryProtocol
from app.infrastructure.pdf_converter import GotenbergPDFConverter
from app.infrastructure.repository import MongoRepository
from app.infrastructure.utils import MongoDocument


class Context(ContextProtocol):
    def __init__(
        self,
        settings: Settings,
        database: AsyncDatabase[MongoDocument],
        session: AsyncClientSession | None = None,
    ):
        self.settings = settings
        self.database = database
        self.session = session

    @cached_property
    def repository(self) -> RepositoryProtocol:
        return MongoRepository(database=self.database, session=self.session)

    @cached_property
    def pdf_converter(self) -> PDFConverterProtocol:
        return GotenbergPDFConverter(host=self.settings.gotenberg_host)
