from typing import Union

from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPBearer
from fastapi_cache.decorator import cache
from pydantic import PositiveInt

from efmarketplace import schemas
from efmarketplace.pkg.types.integeres import PositiveIntWithZero
from efmarketplace.services import country_service
from efmarketplace.services.authorization import auth_only
from efmarketplace.settings import settings

__all__ = [
    "router",
]

router = APIRouter(dependencies=[Depends(auth_only), Security(HTTPBearer())])


@router.get(
    "/",
    response_model=schemas.CountriesWithPagination,
    status_code=status.HTTP_200_OK,
    description="Get all countries.",
)
@cache(expire=settings.cache)
async def read_all_countries(
    cities: bool = False,
    limit: PositiveInt = 10,
    offset: PositiveIntWithZero = 0,
):
    query = schemas.ReadAllCountryQuery(with_cities=cities, limit=limit, offset=offset)
    return await country_service.read_all_countries(query=query)


@router.get(
    "/{country_id}",
    status_code=status.HTTP_200_OK,
    description="Read specific country.",
)
@cache(expire=settings.cache)
async def read_country(
    country_id: int,
    cities: bool = False,
) -> Union[schemas.CountryWithCities, schemas.Country]:
    return await country_service.read_specific_country_by_id(
        query=schemas.ReadCountryByIdQuery(id=country_id, with_cities=cities),
    )


@router.get(
    "/{name}",
    status_code=status.HTTP_200_OK,
    description="Read specific country by name.",
)
@cache(expire=settings.cache)
async def read_country(
    name: str,
    cities: bool = False,
) -> Union[schemas.CountryWithCities, schemas.Country]:
    return await country_service.read_specific_country_by_name(
        query=schemas.ReadCountryByNameQuery(name=name, with_cities=cities),
    )
