from fastapi import FastAPI

from app.api.admin.router import router as admin_router
from app.api.auth.router import router as auth_router
from app.api.docs import add_fastapi_docs
from app.api.handlers import add_exception_handlers
from app.api.lifespan import lifespan_factory
from app.api.resume.router import router as main_router
from app.api.skills.router import router as skills_router
from app.api.utils import mount_static
from app.core.settings import AppEnvironment, Settings


def create_fastapi_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan_factory(settings=settings),
    )

    add_exception_handlers(app=app)
    mount_static(app=app, settings=settings)
    add_fastapi_docs(app=app)

    app.include_router(auth_router)
    app.include_router(main_router)
    app.include_router(admin_router)
    app.include_router(skills_router)

    if settings.environment == AppEnvironment.PRODUCTION:
        app.frontend("/", directory="dist")

    return app
