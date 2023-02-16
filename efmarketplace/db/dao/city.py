from typing import List, Union

from tortoise import models

from .base import BaseDAO
from efmarketplace import schemas
from efmarketplace.db.models.city import City

__all__ = ['CityDAO']


class CityDAO(BaseDAO):
    def get_model(self) -> models.Model:
        return City

    async def read(self,
                   query: schemas.ReadCityByIdQuery,
                   orm_obj: bool = False) -> Union[schemas.City, City]:
        c = await City.get(id=query.id)
        return c if orm_obj else schemas.City.from_orm(c)

    async def read_by_name(self,
                           query: schemas.ReadCityByNameQuery,
                           orm_obj: bool = False
                           ) -> Union[schemas.City, City]:
        c = await City.get(name=query.name)
        return c if orm_obj else schemas.City.parse_obj(c)

    async def read_all(self) -> List[schemas.City]:
        c = await City.all()
        return [schemas.City.from_orm(item) for item in c]
