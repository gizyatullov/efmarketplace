from typing import List, Union

from efmarketplace import schemas
from efmarketplace.db.models.category import Category
from efmarketplace.db.models.subcategory import Subcategory
from efmarketplace.web.api import exceptions

from .base import BaseDAO

__all__ = [
    "SubcategoryDAO",
]


class SubcategoryDAO(BaseDAO):
    @staticmethod
    async def create(cmd: schemas.CreateSubcategoryCommand) -> schemas.Subcategory:
        if not await Category.exists(id=cmd.category_id):
            raise exceptions.NotFound(
                message=f"Not found category with ID {cmd.category_id}"
            )
        s = await Subcategory.create(**cmd.dict())
        return schemas.Subcategory.from_orm(s)

    @staticmethod
    async def read(
        query: schemas.ReadSubcategoryByIdQuery, orm_obj: bool = False
    ) -> Union[schemas.Subcategory, Subcategory]:
        s = await Subcategory.get(id=query.id)
        return s if orm_obj else schemas.Subcategory.from_orm(s)

    @staticmethod
    async def read_by_name(
        query: schemas.ReadSubcategoryByNameQuery, orm_obj: bool = False
    ) -> Union[schemas.Subcategory, Subcategory]:
        s = await Subcategory.get(name=query.name)
        return s if orm_obj else schemas.Subcategory.from_orm(s)

    @staticmethod
    async def read_all() -> List[schemas.Subcategory]:
        s = await Subcategory.all()
        return [schemas.Subcategory.from_orm(item) for item in s]
