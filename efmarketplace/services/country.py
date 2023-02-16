from typing import List, Union

from efmarketplace import schemas
from efmarketplace.db.dao import CountryDAO

__all__ = ['CountryService', ]


class CountryService:
    repository: CountryDAO

    def __init__(self, country_repository: CountryDAO):
        self.repository = country_repository

    async def read_all_countries(self,
                                 query: schemas.ReadAllCountryQuery
                                 ) -> List[schemas.CountryWithCities]:
        return await self.repository.read_all(query=query)

    async def read_specific_country_by_name(
        self,
        query: schemas.ReadCountryByNameQuery
    ) -> Union[schemas.CountryWithCities, schemas.Country]:
        return await self.repository.read_by_name(query=query)

    async def read_specific_country_by_id(
        self,
        query: schemas.ReadCountryByIdQuery,
    ) -> Union[schemas.CountryWithCities, schemas.Country]:
        return await self.repository.read(query=query)
