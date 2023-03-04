from typing import List

from pydantic import Field, PositiveInt

from efmarketplace.pkg.types import LowerStr, NotEmptyStr
from efmarketplace.pkg.types.integeres import PositiveIntWithZero

from .base import BaseModel
from .general import ForPaginationFields

__all__ = [
    "SubcategoryFields",
    "Subcategory",
    "CreateSubcategoryCommand",
    "SubcategoriesWithPagination",
    "ReadAllSubcategoryQuery",
    "ReadSubcategoryByNameQuery",
    "ReadSubcategoryByIdQuery",
]


class SubcategoryFields:
    id = Field(description="Subcategory ID", example=2)
    name = Field(description="Subcategory name", example="smartphones")
    category_id = Field(description="Category ID", example=1)


class BaseSubcategory(BaseModel):
    """Base model for subcategory."""

    class Config:
        orm_mode = True


class Subcategory(BaseSubcategory):
    id: PositiveInt = SubcategoryFields.id
    name: NotEmptyStr = SubcategoryFields.name
    category_id: PositiveInt = SubcategoryFields.category_id


class SubcategoriesWithPagination(BaseSubcategory):
    items: List[Subcategory]
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


# Commands.
class CreateSubcategoryCommand(BaseSubcategory):
    name: LowerStr = SubcategoryFields.name
    category_id: PositiveInt = SubcategoryFields.category_id


# Query
class ReadAllSubcategoryQuery(BaseSubcategory):
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0


class ReadSubcategoryByNameQuery(BaseSubcategory):
    name: LowerStr = SubcategoryFields.name


class ReadSubcategoryByIdQuery(BaseSubcategory):
    id: PositiveInt = SubcategoryFields.id
