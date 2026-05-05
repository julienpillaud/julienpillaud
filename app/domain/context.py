from typing import Protocol

from app.domain.cache_manager import CacheManagerProtocol
from app.domain.pdf_converter import PDFConverterProtocol
from app.domain.repository import RepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def repository(self) -> RepositoryProtocol: ...

    @property
    def cache_manager(self) -> CacheManagerProtocol: ...

    @property
    def pdf_converter(self) -> PDFConverterProtocol: ...
