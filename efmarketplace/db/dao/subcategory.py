from typing import List, Union

from tortoise import models
from .base import BaseDAO
from efmarketplace import schemas
from efmarketplace.db.models.subcategory import Subcategory

__all__ = ['SubcategoryDAO', ]


class SubcategoryDAO(BaseDAO):
    def get_model(self) -> models.Model:
        return Subcategory

    async def create(self,
                     cmd: schemas.CreateSubcategoryCommand) -> schemas.Subcategory:
        s = Subcategory(
            **cmd.dict()
        )
        await s.save()
        return schemas.Subcategory.from_orm(s)

    async def read(self,
                   query: schemas.ReadSubcategoryByIdQuery,
                   orm_obj: bool = False) -> Union[schemas.Subcategory, Subcategory]:
        s = await Subcategory.get(id=query.id)
        return s if orm_obj else schemas.Subcategory.from_orm(s)

    async def read_by_name(self,
                           query: schemas.ReadSubcategoryByNameQuery,
                           orm_obj: bool = False
                           ) -> Union[schemas.Subcategory, Subcategory]:
        s = await Subcategory.get(name=query.name)
        return s if orm_obj else schemas.Subcategory.from_orm(s)

    async def read_all(self) -> List[schemas.Subcategory]:
        s = await Subcategory.all()
        return [schemas.Subcategory.from_orm(item) for item in s]
