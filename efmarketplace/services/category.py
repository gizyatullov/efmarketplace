from typing import List, Type

from efmarketplace import schemas
from efmarketplace.db.dao.category import CategoryDAO

__all__ = [
    "CategoryService",
]


class CategoryService:
    repository: Type[CategoryDAO]

    def __init__(self, category_repository: Type[CategoryDAO]):
        self.repository = category_repository

    async def create_category(
        self, cmd: schemas.CreateCategoryCommand
    ) -> schemas.Category:
        return await self.repository.create(cmd=cmd)

    async def read_all_categories(self) -> List[schemas.Category]:
        return await self.repository.read_all()

    async def read_specific_category_by_name(
        self, query: schemas.ReadCategoryByNameQuery
    ) -> schemas.Category:
        return await self.repository.read_by_name(query=query)

    async def read_specific_category_by_id(
        self, query: schemas.ReadCategoryByIdQuery
    ) -> schemas.Category:
        return await self.repository.read(query=query)
