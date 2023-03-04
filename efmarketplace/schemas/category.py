from typing import List

from pydantic import Field, PositiveInt

from efmarketplace.pkg.types import LowerStr, NotEmptyStr
from efmarketplace.pkg.types.integeres import PositiveIntWithZero

from .base import BaseModel
from .general import ForPaginationFields

__all__ = [
    "CategoryFields",
    "Category",
    "CategoriesWithPagination",
    "CreateCategoryCommand",
    "ReadAllCategoryQuery",
    "ReadCategoryByNameQuery",
    "ReadCategoryByIdQuery",
]


class CategoryFields:
    id = Field(description="Category ID", example=2)
    name = Field(description="Category name", example="non-food")


class BaseCategory(BaseModel):
    """Base model for category."""

    class Config:
        orm_mode = True


class Category(BaseCategory):
    id: PositiveInt = CategoryFields.id
    name: NotEmptyStr = CategoryFields.name


class CategoriesWithPagination(BaseCategory):
    items: List[Category]
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


# Commands.
class CreateCategoryCommand(BaseCategory):
    name: LowerStr = CategoryFields.name


# Query
class ReadAllCategoryQuery(BaseCategory):
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0


class ReadCategoryByNameQuery(BaseCategory):
    name: LowerStr = CategoryFields.name


class ReadCategoryByIdQuery(BaseCategory):
    id: PositiveInt = CategoryFields.id
