from pydantic import Field, PositiveInt

from efmarketplace.pkg.types.integeres import PositiveIntWithZero

from .base import BaseModel

__all__ = [
    "ForPaginationFields",
    "PaginationMixin",
    "ReadAllQueryMixin",
]


class ForPaginationFields:
    total = Field(description="Total items in the selection.", example=101)
    page = Field(description="Current page.", example=2)
    size = Field(description="Requested number of items per page.", example=10)


class PaginationMixin(BaseModel):
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


class ReadAllQueryMixin:
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0
