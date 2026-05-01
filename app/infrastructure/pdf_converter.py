from collections.abc import AsyncIterator

import httpx

from app.domain.pdf_converter import PDFConverterProtocol


class GotenbergPDFConverter(PDFConverterProtocol):
    def __init__(self, host: str) -> None:
        self.host = host
        self.converter_url = f"{host}/forms/chromium/convert/html"
        self.options = {
            "marginTop": "0",
            "marginBottom": "0",
            "marginLeft": "0",
            "marginRight": "0",
            "preferCssPageSize": "true",
        }

    async def stream_pdf(
        self,
        html: str,
        /,
        timeout: float = 60,
        chunk_size: int = 65536,
    ) -> AsyncIterator[bytes]:
        async with (
            httpx.AsyncClient() as client,
            client.stream(
                "POST",
                self.converter_url,
                files={"files": ("index.html", html, "text/html")},
                data=self.options,
                timeout=timeout,
            ) as response,
        ):
            response.raise_for_status()
            async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                yield chunk
