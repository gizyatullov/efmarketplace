from typing import List

from efmarketplace import schemas
from efmarketplace.db.dao import SubcategoryDAO

__all__ = ['SubcategoryService', ]


class SubcategoryService:
    repository: SubcategoryDAO

    def __init__(self, subcategory_repository: SubcategoryDAO):
        self.repository = subcategory_repository

    async def create_subcategory(self,
                                 cmd: schemas.CreateSubcategoryCommand
                                 ) -> schemas.Subcategory:
        return await self.repository.create(cmd=cmd)

    async def read_all_subcategories(self) -> List[schemas.Subcategory]:
        return await self.repository.read_all()

    async def read_specific_subcategory_by_name(self,
                                                query: schemas.ReadSubcategoryByNameQuery
                                                ) -> schemas.Subcategory:
        return await self.repository.read_by_name(query=query)

    async def read_specific_subcategory_by_id(self,
                                              query: schemas.ReadSubcategoryByIdQuery
                                              ) -> schemas.Subcategory:
        return await self.repository.read(query=query)
