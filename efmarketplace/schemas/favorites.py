from typing import List

from pydantic import Field, PositiveInt

from .base import BaseModel
from .user import UserFields, UserIDMixin
from .general import PaginationMixin, ReadAllQueryMixin

__all__ = [
    "FavoritesFields",
    "Favorites",
    "FavoritesWithPagination",
    "ReadAllFavoritesQuery",
    "AddFavoritesCommand",
    "AddFavoritesWithUserIDCommand",
    "DelFavoritesCommand",
    "DelFavoritesWithUserIDCommand",
]


class FavoritesFields:
    id = Field(description="Row ID.", example=2)
    product_id = Field(description="Product ID.", example=2)


class BaseFavorites(BaseModel):
    """Base schema for Favorites."""

    class Config:
        orm_mode = True


class Favorites(BaseFavorites):
    id: PositiveInt = FavoritesFields.id
    user_id: PositiveInt = UserFields.id
    product_id: PositiveInt = FavoritesFields.product_id


class FavoritesWithPagination(PaginationMixin, BaseFavorites):
    items: List[Favorites]


# Query
class ReadAllFavoritesQuery(ReadAllQueryMixin, BaseFavorites):
    user_id: PositiveInt = UserFields.id


# Command
class AddFavoritesCommand(BaseFavorites):
    product_id: PositiveInt = FavoritesFields.product_id


class AddFavoritesWithUserIDCommand(UserIDMixin, AddFavoritesCommand):
    pass


class DelFavoritesCommand(BaseFavorites):
    product_id: PositiveInt = FavoritesFields.product_id


class DelFavoritesWithUserIDCommand(UserIDMixin, DelFavoritesCommand):
    pass
