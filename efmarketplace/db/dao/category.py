from typing import List, Union

from tortoise import models

from efmarketplace import schemas
from efmarketplace.db.models.category import Category

from .base import BaseDAO

__all__ = [
    "CategoryDAO",
]


class CategoryDAO(BaseDAO):
    @staticmethod
    async def create(cmd: schemas.CreateCategoryCommand) -> schemas.Category:
        c = await Category.create(**cmd.dict())
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
    async def read_all(
        query: schemas.ReadAllCategoryQuery,
    ) -> schemas.CategoriesWithPagination:
        c = (
            await Category.all()
            .limit(query.limit)
            .filter(id__gt=query.limit * query.offset)
            .order_by("id")
        )
        total = await Category.all().count()
        return schemas.CategoriesWithPagination(
            items=[schemas.Category.from_orm(item) for item in c],
            total=total,
            page=query.offset,
            size=query.limit,
        )
