from typing import List

from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPBearer

from efmarketplace import schemas
from efmarketplace.services import city_service
from efmarketplace.services.authorization import auth_only

__all__ = [
    "router",
]

router = APIRouter(dependencies=[Depends(auth_only), Security(HTTPBearer())])


@router.get(
    "/",
    response_model=List[schemas.City],
    status_code=status.HTTP_200_OK,
    description="Get all cities.",
)
async def read_all_cities():
    return await city_service.read_all_cities()


@router.get(
    "/{city_id:int}",
    response_model=schemas.City,
    status_code=status.HTTP_200_OK,
    description="Read specific city.",
)
async def read_city(
    city_id: int = schemas.CityFields.id,
):
    return await city_service.read_specific_city_by_id(
        query=schemas.ReadCityByIdQuery(id=city_id),
    )


@router.get(
    "/{name:str}",
    response_model=schemas.City,
    status_code=status.HTTP_200_OK,
    description="Read specific city by name.",
)
async def read_city(
    name: str = schemas.CityFields.name,
):
    return await city_service.read_specific_city_by_name(
        query=schemas.ReadCityByNameQuery(name=name),
    )
