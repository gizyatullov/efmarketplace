from fastapi import APIRouter, status
from fastapi.param_functions import Depends, Security
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from pydantic import PositiveInt

from efmarketplace import schemas
from efmarketplace.db.dao.favorites import FavoritesDAO
from efmarketplace.pkg.types.integeres import PositiveIntWithZero
from efmarketplace.services.authorization import auth_only

__all__ = [
    "router",
]

router = APIRouter(dependencies=[Depends(auth_only), Security(HTTPBearer())])


@router.get(
    "/all",
    response_model=schemas.FavoritesWithPagination,
    status_code=status.HTTP_200_OK,
    description="Read all user favorites.",
)
async def get_all_favorites(
    limit: PositiveInt = 10,
    offset: PositiveIntWithZero = 0,
    favorites_dao: FavoritesDAO = Depends(),
    authorize: AuthJWT = Depends(),
):
    user_id = authorize.get_raw_jwt().get("uid", "")
    query = schemas.ReadAllFavoritesQuery(limit=limit, offset=offset, user_id=user_id)
    return await favorites_dao.read_all(query=query)


@router.post(
    "/add",
    response_model=schemas.Favorites,
    status_code=status.HTTP_200_OK,
    description="Add user favorites.",
)
async def add_favorites(
    cmd: schemas.AddFavoritesCommand,
    favorites_dao: FavoritesDAO = Depends(),
    authorize: AuthJWT = Depends(),
):
    user_id = authorize.get_raw_jwt().get("uid", "")
    cmd = schemas.AddFavoritesWithUserIDCommand(**cmd.dict(), user_id=user_id)
    return await favorites_dao.add(cmd=cmd)


@router.delete(
    "/delete",
    response_model=schemas.Favorites,
    status_code=status.HTTP_202_ACCEPTED,
    description="Del user favorites.",
)
async def del_favorites(
    cmd: schemas.DelFavoritesCommand,
    favorites_dao: FavoritesDAO = Depends(),
    authorize: AuthJWT = Depends(),
):
    user_id = authorize.get_raw_jwt().get("uid", "")
    cmd = schemas.DelFavoritesWithUserIDCommand(**cmd.dict(), user_id=user_id)
    return await favorites_dao.delete(cmd=cmd)
