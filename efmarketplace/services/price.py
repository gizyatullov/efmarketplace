from typing import Dict, List

from fastapi import status
from redis.asyncio import ConnectionPool, Redis
import httpx

from efmarketplace import schemas
from efmarketplace.web.api.exceptions.price import ServiceIsUnavailable
from efmarketplace.settings import settings

__all__ = [
    "PriceService",
]


class PriceService:
    async def _get_price_with_binance(
        self, query: schemas.ReadPriceQuery = schemas.ReadPriceQuery()
    ) -> List[schemas.UnitPrice]:
        units_price = []
        base_uri = "https://www.binance.com/api/v3/ticker/price?symbol="
        async with httpx.AsyncClient() as client:
            for name in query.currencies:
                r = await client.get(url=f"{base_uri}{name}")
                payload = r.json()
                if not r.status_code == status.HTTP_200_OK or not payload.get("price"):
                    continue
                units_price.append(
                    schemas.UnitPrice(name_pair=name, price=payload.get("price"))
                )
        return units_price

    async def _set_price_in_redis(
        self,
        query: List[schemas.UnitPrice],
    ) -> None:
        async with Redis().from_url(url=str(settings.redis_url)) as r:
            for item in query:
                await r.set(
                    name=f"{item.prefix_in_redis}{item.name_pair}", value=item.price
                )

    async def set_price(self) -> None:
        units_price = await self._get_price_with_binance()
        await self._set_price_in_redis(query=units_price)

    async def _read_price_in_redis(
        self, redis_pool: ConnectionPool, query: schemas.ReadPriceQuery
    ) -> Dict[str, str]:
        result = {}
        async with Redis(connection_pool=redis_pool) as redis:
            for name in query.currencies:
                v: bytes = await redis.get(name=f"{query.prefix_in_redis}{name}")
                if v:
                    result[name.upper()] = v.decode(encoding="utf-8")
                else:
                    raise ServiceIsUnavailable
        return result

    async def read_price(
        self, query: schemas.ReadPriceQuery, redis_pool: ConnectionPool
    ) -> schemas.Price:
        prices = await self._read_price_in_redis(query=query, redis_pool=redis_pool)
        return schemas.Price(BTC=schemas.BTC(**prices))
