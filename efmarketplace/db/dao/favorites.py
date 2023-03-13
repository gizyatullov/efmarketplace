from efmarketplace import schemas
from efmarketplace.db import models

from .base import BaseDAO

__all__ = [
    "FavoritesDAO",
]

Model = models.Favorites
Schema = schemas.Favorites
ReadAllFavoritesQuery = schemas.ReadAllFavoritesQuery
AddFavoritesWithUserIDCommand = schemas.AddFavoritesWithUserIDCommand
DelFavoritesWithUserIDCommand = schemas.DelFavoritesWithUserIDCommand


class FavoritesDAO(BaseDAO[Model]):
    _model = Model

    @staticmethod
    async def read_all(query: ReadAllFavoritesQuery) -> schemas.FavoritesWithPagination:
        f = await Model.filter(
            user_id=query.user_id, id__gt=query.limit * query.offset
        ).limit(query.limit)
        return schemas.FavoritesWithPagination(
            items=[Schema.from_orm(item) for item in f],
            total=len(f),
            page=query.offset,
            size=query.limit,
        )

    @staticmethod
    async def add(cmd: AddFavoritesWithUserIDCommand) -> schemas.Favorites:
        f = await Model.create(user_id=cmd.user_id, product_id=cmd.product_id)
        return schemas.Favorites.from_orm(f)

    @staticmethod
    async def delete(cmd: DelFavoritesWithUserIDCommand) -> schemas.Favorites:
        f = await Model.get(user_id=cmd.user_id, product_id=cmd.product_id)
        await f.delete()
        return schemas.Favorites.from_orm(f)
