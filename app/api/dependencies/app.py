from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pymongo.asynchronous.client_session import AsyncClientSession

from app.core.context import Context, ContextFactory
from app.core.domain import Domain
from app.core.settings import Settings
from app.domain.pdf_converter import PDFConverterProtocol
from app.infrastructure.mongo_repository.resource.asynchronous import AsyncMongoResource
from app.infrastructure.pdf_converter import GotenbergPDFConverter


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_templates(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Jinja2Templates:
    return Jinja2Templates(directory=settings.paths.templates)


def get_pdf_converter(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> PDFConverterProtocol:
    http_client = request.app.state.http_client
    return GotenbergPDFConverter(
        client=http_client,
        host=settings.gotenberg_host,
    )


def get_mongo_resource(request: Request) -> AsyncMongoResource:
    resource = request.app.state.mongo_resource
    if not isinstance(resource, AsyncMongoResource):
        raise RuntimeError()

    return resource


def get_context_factory(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> ContextFactory:
    mongo_client = request.app.state.mongo_resource.client

    def _get_context(session: AsyncClientSession | None) -> Context:
        return Context(
            settings=settings,
            redis_client=request.app.state.redis_client,
            database=mongo_client[settings.mongo_database],
            session=session,
        )

    return _get_context


async def get_domain(
    mongo_resource: Annotated[AsyncMongoResource, Depends(get_mongo_resource)],
    context_factory: Annotated[ContextFactory, Depends(get_context_factory)],
) -> AsyncIterator[Domain]:
    async with Domain(
        resource=mongo_resource,
        context_factory=context_factory,
    ) as domain:
        yield domain
