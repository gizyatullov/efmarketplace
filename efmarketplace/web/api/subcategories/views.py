from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPBearer
from fastapi_cache.decorator import cache
from pydantic import PositiveInt

from efmarketplace import schemas
from efmarketplace.pkg.types.integeres import CustPositiveInt, PositiveIntWithZero
from efmarketplace.pkg.types.strings import NotEmptyStr
from efmarketplace.services import subcategory_service
from efmarketplace.services.authorization import auth_only
from efmarketplace.settings import settings

__all__ = [
    "router",
]

router = APIRouter(dependencies=[Depends(auth_only), Security(HTTPBearer())])


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
    response_model=schemas.SubcategoriesWithPagination,
    status_code=status.HTTP_200_OK,
    description="Get all subcategories.",
)
@cache(expire=settings.cache)
async def read_all_subcategories(
    limit: PositiveInt = 10,
    offset: PositiveIntWithZero = 0,
):
    query = schemas.ReadAllSubcategoryQuery(limit=limit, offset=offset)
    return await subcategory_service.read_all_subcategories(query=query)


@router.get(
    "/{subcategory_id}",
    response_model=schemas.Subcategory,
    status_code=status.HTTP_200_OK,
    description="Read specific subcategory by id.",
)
@cache(expire=settings.cache)
async def read_subcategory(subcategory_id: CustPositiveInt):
    return await subcategory_service.read_specific_subcategory_by_id(
        query=schemas.ReadSubcategoryByIdQuery(id=subcategory_id),
    )


@router.get(
    "/{name}",
    response_model=schemas.Subcategory,
    status_code=status.HTTP_200_OK,
    description="Read specific subcategory by name.",
)
@cache(expire=settings.cache)
async def read_subcategory(name: NotEmptyStr):
    return await subcategory_service.read_specific_subcategory_by_name(
        query=schemas.ReadSubcategoryByNameQuery(name=name),
    )
