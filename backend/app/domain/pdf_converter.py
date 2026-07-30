from collections.abc import AsyncIterator
from typing import Protocol


class PDFConverterProtocol(Protocol):
    def stream_pdf(
        self,
        html: str,
        /,
        timeout: float = 60,
        chunk_size: int = 65536,
    ) -> AsyncIterator[bytes]: ...
