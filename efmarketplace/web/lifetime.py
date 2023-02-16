from typing import Awaitable, Callable

from fastapi import FastAPI

from efmarketplace.services.redis.lifetime import init_redis, shutdown_redis
from efmarketplace.services.repeat import init_repeaters


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event('startup')
    async def _startup() -> None:  # noqa: WPS430
        init_redis(app)
        init_repeaters(app)

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event('shutdown')
    async def _shutdown() -> None:  # noqa: WPS430
        await shutdown_redis(app)

    return _shutdown
