from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPBearer
from fastapi_cache.decorator import cache
from pydantic import PositiveInt

from efmarketplace import schemas
from efmarketplace.pkg.types.integeres import PositiveIntWithZero
from efmarketplace.services import city_service
from efmarketplace.services.authorization import auth_only
from efmarketplace.settings import settings

__all__ = [
    "router",
]

router = APIRouter(dependencies=[Depends(auth_only), Security(HTTPBearer())])


@router.get(
    "/",
    response_model=schemas.CitiesWithPagination,
    status_code=status.HTTP_200_OK,
    description="Get all cities.",
)
@cache(expire=settings.cache)
async def read_all_cities(
    limit: PositiveInt = 10,
    offset: PositiveIntWithZero = 0,
):
    query = schemas.ReadAllCityQuery(limit=limit, offset=offset)
    return await city_service.read_all_cities(query=query)


@router.get(
    "/{city_id}",
    response_model=schemas.City,
    status_code=status.HTTP_200_OK,
    description="Read specific city.",
)
@cache(expire=settings.cache)
async def read_city(city_id: int):
    return await city_service.read_specific_city_by_id(
        query=schemas.ReadCityByIdQuery(id=city_id),
    )


@router.get(
    "/{name}",
    response_model=schemas.City,
    status_code=status.HTTP_200_OK,
    description="Read specific city by name.",
)
@cache(expire=settings.cache)
async def read_city(name: str):
    return await city_service.read_specific_city_by_name(
        query=schemas.ReadCityByNameQuery(name=name),
    )
