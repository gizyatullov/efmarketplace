import uvicorn
from efmarketplace.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "efmarketplace.web.application:get_app",
        workers=settings.WORKERS_COUNT,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.UVICORN_RELOAD,
        log_level=settings.LOG_LEVEL.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
