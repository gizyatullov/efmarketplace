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
        return c if orm_obj else Schema.from_orm(c)

    @staticmethod
    async def read_all(query: schemas.ReadAllCityQuery) -> schemas.CitiesWithPagination:
        c = (
            await Model.all()
            .limit(query.limit)
            .filter(id__gt=query.limit * query.offset)
            .order_by("id")
        )
        total = await Model.all().count()
        return schemas.CitiesWithPagination(
            items=[Schema.from_orm(item) for item in c],
            total=total,
            page=query.offset,
            size=query.limit,
        )
