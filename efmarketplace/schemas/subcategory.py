from pydantic import Field, PositiveInt

from .base import BaseModel
from efmarketplace.pkg.types import NotEmptyStr, LowerStr

__all__ = [
    'SubcategoryFields',
    'Subcategory',
    'CreateSubcategoryCommand',
    'ReadSubcategoryByNameQuery',
    'ReadSubcategoryByIdQuery',
]


class SubcategoryFields:
    id = Field(description='Subcategory ID', example=2)
    name = Field(description='Subcategory name', example='smartphones')
    category_id = Field(description='Category ID', example=1)


class BaseSubcategory(BaseModel):
    """Base model for subcategory."""

    class Config:
        orm_mode = True


class Subcategory(BaseSubcategory):
    id: PositiveInt = SubcategoryFields.id
    name: NotEmptyStr = SubcategoryFields.name
    category_id: PositiveInt = SubcategoryFields.category_id


# Commands.
class CreateSubcategoryCommand(BaseSubcategory):
    name: LowerStr = SubcategoryFields.name
    category_id: PositiveInt = SubcategoryFields.category_id


# Query
class ReadSubcategoryByNameQuery(BaseSubcategory):
    name: LowerStr = SubcategoryFields.name


class ReadSubcategoryByIdQuery(BaseSubcategory):
    id: PositiveInt = SubcategoryFields.id
