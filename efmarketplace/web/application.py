from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth.exceptions import AuthJWTException
from tortoise.contrib.fastapi import register_tortoise

from efmarketplace.db.config import TORTOISE_CONFIG
from efmarketplace.logging_ import configure_logging
from efmarketplace.settings import settings
from efmarketplace.web.api.exceptions.base import BaseAPIException
from efmarketplace.web.api.router import api_router
from efmarketplace.web.handle_http_exceptions import (
    authjwt_exception_handler,
    handle_api_exceptions,
)
from efmarketplace.web.lifetime import register_shutdown_event, register_startup_event

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title=settings.APP_NAME,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
        generate_schemas=True,
    )

    app.add_exception_handler(BaseAPIException, handle_api_exceptions)
    app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

    return app
