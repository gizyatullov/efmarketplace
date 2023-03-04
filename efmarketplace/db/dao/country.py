from typing import Literal, Union, overload

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
SchemaCityWithoutCountryID = schemas.CityWithoutCountryID


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
            c = await Model.get(id=query.id).prefetch_related("cities")
            if orm_obj:
                return c
            obj = dict(c)
            obj["cities"] = list(c.cities)
            return SchemaWithCities.parse_obj(obj)

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
            c = await Model.get(name=query.name).prefetch_related("cities")
            if orm_obj:
                return c
            obj = dict(c)
            obj["cities"] = list(c.cities)
            return SchemaWithCities.parse_obj(obj)

        c = await Model.get(name=query.name)
        return c if orm_obj else Schema.from_orm(c)

    @staticmethod
    async def read_all(
        query: ReadAllCountryQuery,
    ) -> schemas.CountriesWithPagination:
        total = await Model.all().count()
        if query.with_cities:
            c = (
                await Model.all()
                .prefetch_related("cities")
                .limit(query.limit)
                .filter(id__gt=query.limit * query.offset)
                .order_by("id")
            )
            result = []
            for item in c:
                el = SchemaWithCities.parse_obj(item)
                el.cities = [
                    SchemaCityWithoutCountryID.from_orm(city) for city in item.cities
                ]
                result.append(el)
            return schemas.CountriesWithPagination(
                items=result, total=total, page=query.offset, size=query.limit
            )

        c = (
            await Model.all()
            .limit(query.limit)
            .filter(id__gt=query.limit * query.offset)
            .order_by("id")
        )
        return schemas.CountriesWithPagination(
            items=[Schema.from_orm(item) for item in c],
            total=total,
            page=query.offset,
            size=query.limit,
        )
