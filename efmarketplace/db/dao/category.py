from typing import List, Union

from tortoise import models

from .base import BaseDAO
from efmarketplace import schemas
from efmarketplace.db.models.category import Category

__all__ = [
    "CategoryDAO",
]


class CategoryDAO(BaseDAO):
    @staticmethod
    async def create(cmd: schemas.CreateCategoryCommand) -> schemas.Category:
        c = Category(**cmd.dict())
        await c.save()
        return schemas.Category.from_orm(c)

    @staticmethod
    async def read(
        query: schemas.ReadCategoryByIdQuery, orm_obj: bool = False
    ) -> Union[schemas.Category, Category]:
        c = await Category.get(id=query.id)
        return c if orm_obj else schemas.Category.from_orm(c)

    @staticmethod
    async def read_by_name(
        query: schemas.ReadCategoryByNameQuery, orm_obj: bool = False
    ) -> Union[schemas.Category, Category]:
        c = await Category.get(name=query.name)
        return c if orm_obj else schemas.Category.from_orm(c)

    @staticmethod
    async def read_all() -> List[schemas.Category]:
        c = await Category.all()
        return [schemas.Category.from_orm(item) for item in c]
