from pydantic import Field, PositiveInt

from .base import BaseModel
from efmarketplace.pkg.types.strings import LowerStr

__all__ = [
    'CityFields',
    'City',
    'CityWithoutCountryID',
    'ReadCityByNameQuery',
    'ReadCityByIdQuery',
]


class CityFields:
    id = Field(description='City ID', example=2)
    name = Field(description='City name', example='dimitrovgrad')
    country_id = Field(description='Country ID', example=2)


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


# Query
class ReadCityByNameQuery(BaseCity):
    name: LowerStr = CityFields.name


class ReadCityByIdQuery(BaseCity):
    id: PositiveInt = CityFields.id
