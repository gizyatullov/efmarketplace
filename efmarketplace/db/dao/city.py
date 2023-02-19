from typing import List, Literal, Union, overload

from efmarketplace import schemas
from efmarketplace.db import models
from efmarketplace.schemas import ReadCityByIdQuery, ReadCityByNameQuery

from .base import BaseDAO

__all__ = ["CityDAO"]

Model = models.City
Schema = schemas.City


class CityDAO(BaseDAO[models.City]):
    _model = Model

    @staticmethod
    @overload
    async def read(query: ReadCityByIdQuery, orm_obj: Literal[True]) -> Model:
        ...

    @staticmethod
    @overload
    async def read(query: ReadCityByIdQuery, orm_obj: Literal[False]) -> Schema:
        ...

    @staticmethod
    async def read(
        query: ReadCityByIdQuery, orm_obj: bool = False
    ) -> Union[Schema, Model]:
        c = await Model.get(id=query.id)
        return c if orm_obj else Schema.from_orm(c)

    @staticmethod
    async def read_by_name(
        query: ReadCityByNameQuery, orm_obj: bool = False
    ) -> Union[Schema, Model]:
        c = await Model.get(name=query.name)
        return c if orm_obj else Schema.parse_obj(c)

    @staticmethod
    async def read_all() -> List[Schema]:
        c = await Model.all()
        return [Schema.from_orm(item) for item in c]
