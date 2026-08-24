from typing import Any

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response

from app.api.dependencies.user import check_docs_access


def add_fastapi_docs(app: FastAPI) -> None:
    @app.get(
        "/docs",
        dependencies=[Depends(check_docs_access)],
        include_in_schema=False,
    )
    async def get_swagger_ui() -> Response:
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=app.title + " - Swagger UI",
            swagger_ui_parameters={
                "tryItOutEnabled": True,
                "displayRequestDuration": True,
            },
        )

    @app.get(
        "/openapi.json",
        dependencies=[Depends(check_docs_access)],
        include_in_schema=False,
    )
    async def get_swagger_ui_json() -> dict[str, Any]:
        return get_openapi(
            title=app.title,
            version=app.version,
            routes=app.routes,
        )
