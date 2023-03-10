from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPBearer
from fastapi_cache.decorator import cache
from pydantic import PositiveInt

from efmarketplace import schemas
from efmarketplace.pkg.types.integeres import PositiveIntWithZero
from efmarketplace.services import category_service
from efmarketplace.services.authorization import auth_only
from efmarketplace.settings import settings

__all__ = [
    "router",
]

router = APIRouter(dependencies=[Depends(auth_only), Security(HTTPBearer())])


@router.post(
    "/",
    response_model=schemas.Category,
    status_code=status.HTTP_201_CREATED,
    description="Create category",
)
async def create_category(
    cmd: schemas.CreateCategoryCommand,
):
    return await category_service.create_category(cmd=cmd)


@router.get(
    "/",
    response_model=schemas.CategoriesWithPagination,
    status_code=status.HTTP_200_OK,
    description="Get all categories.",
)
@cache(expire=settings.cache)
async def read_all_categories(
    limit: PositiveInt = 10,
    offset: PositiveIntWithZero = 0,
):
    query = schemas.ReadAllCategoryQuery(limit=limit, offset=offset)
    return await category_service.read_all_categories(query=query)


@router.get(
    "/{category_id:int}",
    response_model=schemas.Category,
    status_code=status.HTTP_200_OK,
    description="Read specific category by id.",
)
@cache(expire=settings.cache)
async def read_category(
    category_id: int = schemas.CategoryFields.id,
):
    return await category_service.read_specific_category_by_id(
        query=schemas.ReadCategoryByIdQuery(id=category_id),
    )


@router.get(
    "/{name:str}",
    response_model=schemas.Category,
    status_code=status.HTTP_200_OK,
    description="Read specific category by name.",
)
@cache(expire=settings.cache)
async def read_category(
    name: str = schemas.CategoryFields.name,
):
    return await category_service.read_specific_category_by_name(
        query=schemas.ReadCategoryByNameQuery(name=name),
    )
