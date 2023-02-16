from typing import List, Union

from tortoise import models
from tortoise.contrib.pydantic import pydantic_queryset_creator

from .base import BaseDAO
from efmarketplace import schemas
from efmarketplace.db.models.country import Country

__all__ = ['CountryDAO']


class CountryDAO(BaseDAO):

    def __init__(self):
        self.CountryPydantic = pydantic_queryset_creator(Country)

    def get_model(self) -> models.Model:
        return Country

    async def read(self,
                   query: schemas.ReadCountryByIdQuery,
                   orm_obj: bool = False) -> Union[schemas.CountryWithCities,
                                                   schemas.Country, Country]:
        if query.with_cities:
            q = Country.filter(id=query.id).prefetch_related()
            if orm_obj: return await q.first()
            country_pydantic = pydantic_queryset_creator(Country)
            q = await country_pydantic.from_queryset(q)
            q = q.dict()['__root__'][0]
            return schemas.CountryWithCities.parse_obj(q)

        c = await Country.get(id=query.id)
        return c if orm_obj else schemas.Country.from_orm(c)

    async def read_by_name(self,
                           query: schemas.ReadCountryByNameQuery,
                           orm_obj: bool = False
                           ) -> Union[schemas.CountryWithCities,
                                      schemas.Country, Country]:
        if query.with_cities:
            q = Country.filter(name=query.name).prefetch_related()
            if orm_obj: return await q.first()
            country_pydantic = pydantic_queryset_creator(Country)
            q = await country_pydantic.from_queryset(q)
            q = q.dict()['__root__'][0]
            return schemas.CountryWithCities.parse_obj(q)

        c = await Country.get(name=query.name)
        return c if orm_obj else schemas.Country.from_orm(c)

    async def read_all(self,
                       query: schemas.ReadAllCountryQuery
                       ) -> Union[
        List[schemas.Country], List[schemas.CountryWithCities]]:
        if query.with_cities:
            q = Country.all().prefetch_related()
            country_pydantic = pydantic_queryset_creator(Country)
            q = await country_pydantic.from_queryset(queryset=q)
            q = q.dict()['__root__']
            return [schemas.CountryWithCities.parse_obj(item) for item in q]

        q = await Country.all()
        return [schemas.Country.from_orm(item) for item in q]
