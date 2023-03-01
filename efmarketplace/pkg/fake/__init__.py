from efmarketplace.settings import settings

from .gen import start_fill

__all__ = [
    "fake_fill_db",
]


def fake_fill_db():
    if settings.FILL_TABLES:
        start_fill()
