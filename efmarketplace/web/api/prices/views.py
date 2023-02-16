from fastapi import APIRouter, status, Depends
from redis.asyncio import ConnectionPool

from efmarketplace import schemas
from efmarketplace.services import price_service
from efmarketplace.services.redis.dependency import get_redis_pool

router = APIRouter()

__all__ = [
    'router',
]


@router.post(
    '/',
    name='price',
    response_model=schemas.Price,
    status_code=status.HTTP_200_OK,
    description='Get currency prices.',
)
async def read_price(redis_pool: ConnectionPool = Depends(get_redis_pool)):
    return await price_service.read_price(query=schemas.ReadPriceQuery(),
                                          redis_pool=redis_pool)
