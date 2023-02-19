from typing import List, Type

from efmarketplace import schemas
from efmarketplace.db.dao.city import CityDAO

__all__ = [
    "CityService",
]


class CityService:
    repository: Type[CityDAO]

    def __init__(self, city_repository: Type[CityDAO]):
        self.repository = city_repository

    async def read_all_cities(self) -> List[schemas.City]:
        return await self.repository.read_all()

    async def read_specific_city_by_name(
        self, query: schemas.ReadCityByNameQuery
    ) -> schemas.City:
        return await self.repository.read_by_name(query=query)

    async def read_specific_city_by_id(
        self,
        query: schemas.ReadCityByIdQuery,
    ) -> schemas.City:
        return await self.repository.read(query=query)
