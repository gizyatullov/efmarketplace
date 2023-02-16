import uvicorn

from efmarketplace.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        'efmarketplace.web.application:get_app',
        workers=settings.workers_count,
        host=settings.host,
        port=settings.API_SERVER_PORT,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == '__main__':
    main()
