from typing import List, Literal, Union, overload

from tortoise.contrib.pydantic import pydantic_queryset_creator

from efmarketplace import schemas
from efmarketplace.db import models
from efmarketplace.schemas import (
    ReadAllCountryQuery,
    ReadCountryByIdQuery,
    ReadCountryByNameQuery,
)

from .base import BaseDAO

__all__ = ["CountryDAO"]

Model = models.Country
Schema = schemas.Country
SchemaWithCities = schemas.CountryWithCities


class CountryDAO(BaseDAO[Model]):
    _model = Model

    @staticmethod
    @overload
    async def read(query: ReadCountryByIdQuery, orm_obj: Literal[True]) -> Model:
        ...

    @staticmethod
    @overload
    async def read(
        query: ReadCountryByIdQuery, orm_obj: Literal[False]
    ) -> Union[SchemaWithCities, Schema]:
        ...

    @staticmethod
    async def read(
        query: ReadCountryByIdQuery, orm_obj: bool = False
    ) -> Union[SchemaWithCities, Schema, Model]:
        if query.with_cities:
            q = Model.filter(id=query.id).prefetch_related()
            if orm_obj:
                return await q.first()
            country_pydantic = pydantic_queryset_creator(Model)
            q = await country_pydantic.from_queryset(q)
            q = q.dict()["__root__"][0]
            return SchemaWithCities.parse_obj(q)

        c = await Model.get(id=query.id)
        return c if orm_obj else Schema.from_orm(c)

    @staticmethod
    @overload
    async def read_by_name(
        query: ReadCountryByIdQuery, orm_obj: Literal[True]
    ) -> Model:
        ...

    @staticmethod
    @overload
    async def read_by_name(
        query: ReadCountryByIdQuery, orm_obj: Literal[False]
    ) -> Union[SchemaWithCities, Schema]:
        ...

    @staticmethod
    async def read_by_name(
        query: ReadCountryByNameQuery, orm_obj: bool = False
    ) -> Union[SchemaWithCities, Schema, Model]:
        if query.with_cities:
            q = Model.filter(name=query.name).prefetch_related()
            if orm_obj:
                return await q.first()
            country_pydantic = pydantic_queryset_creator(Model)
            q = await country_pydantic.from_queryset(q)
            q = q.dict()["__root__"][0]
            return SchemaWithCities.parse_obj(q)

        c = await Model.get(name=query.name)
        return c if orm_obj else Schema.from_orm(c)

    @staticmethod
    async def read_all(
        query: ReadAllCountryQuery,
    ) -> Union[List[Schema], List[SchemaWithCities]]:
        if query.with_cities:
            q = Model.all().prefetch_related()
            country_pydantic = pydantic_queryset_creator(Model)
            q = await country_pydantic.from_queryset(queryset=q)
            q = q.dict()["__root__"]
            return [SchemaWithCities.parse_obj(item) for item in q]

        q = await Model.all()
        return [Schema.from_orm(item) for item in q]
