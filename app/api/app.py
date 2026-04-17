from fastapi import FastAPI

from app.api.admin.router import router as admin_router
from app.api.auth.router import router as auth_router
from app.api.handlers import add_exception_handlers
from app.api.middlewares import add_security_middleware
from app.api.resume.router import router as main_router
from app.api.utils import lifespan_factory, mount_static
from app.core.settings import Settings


def create_fastapi_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan_factory(settings=settings),
    )

    add_exception_handlers(app=app, settings=settings)
    add_security_middleware(app=app, settings=settings)
    mount_static(app=app, settings=settings)

    app.include_router(main_router)
    app.include_router(auth_router)
    app.include_router(admin_router)

    return app
