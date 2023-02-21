from typing import List, Union

from fastapi import APIRouter, status

from efmarketplace import schemas
from efmarketplace.services import country_service

__all__ = [
    "router",
]

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get all countries.",
)
async def read_all_countries(
    cities: bool = False,
) -> Union[List[schemas.Country], List[schemas.CountryWithCities]]:
    return await country_service.read_all_countries(
        query=schemas.ReadAllCountryQuery(with_cities=cities)
    )


@router.get(
    "/{country_id:int}",
    status_code=status.HTTP_200_OK,
    description="Read specific country.",
)
async def read_country(
    country_id: int = schemas.CountryFields.id,
    cities: bool = False,
) -> Union[schemas.CountryWithCities, schemas.Country]:
    return await country_service.read_specific_country_by_id(
        query=schemas.ReadCountryByIdQuery(id=country_id, with_cities=cities),
    )


@router.get(
    "/{name:str}",
    status_code=status.HTTP_200_OK,
    description="Read specific country by name.",
)
async def read_country(
    name: str = schemas.CountryFields.name,
    cities: bool = False,
) -> Union[schemas.CountryWithCities, schemas.Country]:
    return await country_service.read_specific_country_by_name(
        query=schemas.ReadCountryByNameQuery(name=name, with_cities=cities),
    )
