from functools import cached_property
from typing import Protocol

from app.domain.pdf_converter import PDFConverterProtocol
from app.domain.repository import RepositoryProtocol


class ContextProtocol(Protocol):
    @cached_property
    def repository(self) -> RepositoryProtocol: ...

    @cached_property
    def pdf_converter(self) -> PDFConverterProtocol: ...
