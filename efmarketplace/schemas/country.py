from typing import List, Optional, Union

from pydantic import Field, PositiveInt

from efmarketplace.pkg.types.integeres import PositiveIntWithZero
from efmarketplace.pkg.types.strings import LowerStr

from .base import BaseModel
from .city import CityWithoutCountryID
from .general import ForPaginationFields

__all__ = [
    "CountryFields",
    "Country",
    "CountriesWithPagination",
    "ReadCountryByNameQuery",
    "ReadCountryByIdQuery",
    "ReadAllCountryQuery",
    "CountryWithCities",
]


class CountryFields:
    id = Field(description="Country id.", example=2)
    name = Field(description="Country name", example="russia")
    with_cities = Field(
        description="With a list of cities?", example=True, default=False
    )


class BaseCountry(BaseModel):
    """Base model for country."""

    class Config:
        orm_mode = True


class Country(BaseCountry):
    id: PositiveInt = CountryFields.id
    name: str = CountryFields.name


class CountryWithCities(Country):
    cities: List[Optional[CityWithoutCountryID]] = []


class CountriesWithPagination(BaseCountry):
    items: List[Union[CountryWithCities, Country]]
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


# Query
class ReadAllCountryQuery(BaseCountry):
    with_cities: bool = False
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0


class ReadCountryByNameQuery(BaseCountry):
    name: LowerStr = CountryFields.name
    with_cities: bool = CountryFields.with_cities


class ReadCountryByIdQuery(BaseCountry):
    id: PositiveInt = CountryFields.id
    with_cities: bool = CountryFields.with_cities
