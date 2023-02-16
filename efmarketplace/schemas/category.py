from pydantic import Field, PositiveInt

from .base import BaseModel
from efmarketplace.pkg.types import NotEmptyStr, LowerStr

__all__ = [
    'CategoryFields',
    'Category',
    'CreateCategoryCommand',
    'ReadCategoryByNameQuery',
    'ReadCategoryByIdQuery',
]


class CategoryFields:
    id = Field(description='Category ID', example=2)
    name = Field(description='Category name', example='non-food')


class BaseCategory(BaseModel):
    """Base model for category."""

    class Config:
        orm_mode = True


class Category(BaseCategory):
    id: PositiveInt = CategoryFields.id
    name: NotEmptyStr = CategoryFields.name


# Commands.
class CreateCategoryCommand(BaseCategory):
    name: LowerStr = CategoryFields.name


# Query
class ReadCategoryByNameQuery(BaseCategory):
    name: LowerStr = CategoryFields.name


class ReadCategoryByIdQuery(BaseCategory):
    id: PositiveInt = CategoryFields.id
