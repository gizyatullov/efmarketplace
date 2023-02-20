from typing import List

from fastapi import APIRouter, status

from efmarketplace import schemas
from efmarketplace.services import subcategory_service

__all__ = [
    "router",
]

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.Subcategory,
    status_code=status.HTTP_201_CREATED,
    description="Create subcategory",
)
async def create_subcategory(
    cmd: schemas.CreateSubcategoryCommand,
):
    return await subcategory_service.create_subcategory(cmd=cmd)


@router.get(
    "/",
    response_model=List[schemas.Subcategory],
    status_code=status.HTTP_200_OK,
    description="Get all subcategories.",
)
async def read_all_subcategories():
    return await subcategory_service.read_all_subcategories()


@router.get(
    "/{subcategory_id:int}",
    response_model=schemas.Subcategory,
    status_code=status.HTTP_200_OK,
    description="Read specific subcategory by id.",
)
async def read_subcategory(
    subcategory_id: int = schemas.SubcategoryFields.id,
):
    return await subcategory_service.read_specific_subcategory_by_id(
        query=schemas.ReadSubcategoryByIdQuery(id=subcategory_id),
    )


@router.get(
    "/{name:str}",
    response_model=schemas.Subcategory,
    status_code=status.HTTP_200_OK,
    description="Read specific subcategory by name.",
)
async def read_subcategory(
    name: str = schemas.SubcategoryFields.name,
):
    return await subcategory_service.read_specific_subcategory_by_name(
        query=schemas.ReadSubcategoryByNameQuery(name=name),
    )
