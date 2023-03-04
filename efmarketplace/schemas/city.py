from typing import List

from pydantic import Field, PositiveInt

from efmarketplace.pkg.types.integeres import PositiveIntWithZero
from efmarketplace.pkg.types.strings import LowerStr

from .base import BaseModel
from .general import ForPaginationFields

__all__ = [
    "CityFields",
    "City",
    "CitiesWithPagination",
    "CityWithoutCountryID",
    "ReadAllCityQuery",
    "ReadCityByNameQuery",
    "ReadCityByIdQuery",
]


class CityFields:
    id = Field(description="City ID", example=2)
    name = Field(description="City name", example="dimitrovgrad")
    country_id = Field(description="Country ID", example=2)


class BaseCity(BaseModel):
    """Base model for city."""

    class Config:
        orm_mode = True


class City(BaseCity):
    id: PositiveInt = CityFields.id
    name: str = CityFields.name
    country_id: PositiveInt = CityFields.country_id


class CityWithoutCountryID(BaseCity):
    id: PositiveInt = CityFields.id
    name: str = CityFields.name


class CitiesWithPagination(BaseCity):
    items: List[City]
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


# Query
class ReadAllCityQuery(BaseCity):
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0


class ReadCityByNameQuery(BaseCity):
    name: LowerStr = CityFields.name


class ReadCityByIdQuery(BaseCity):
    id: PositiveInt = CityFields.id
