from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from loguru import logger

from efmarketplace.settings import settings
from efmarketplace.services import price_service


def init_price_update_repeater(app: FastAPI) -> None:
    @app.on_event("startup")
    @repeat_every(seconds=60 * settings.FREQUENCY_PRICE_UPDATES,
                  logger=logger)
    async def run_update_price():
        await price_service.set_price()
        logger.info(f"price update, {settings.FREQUENCY_PRICE_UPDATES} "
                    f"minutes have passed or first start")
