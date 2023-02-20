from typing import List

from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from redis.asyncio import ConnectionPool

from efmarketplace import schemas
from efmarketplace.services import auth_service, user_service, notification_service
from efmarketplace.services.redis.dependency import get_redis_pool
from efmarketplace.web.api.exceptions.auth import IncorrectCaptcha

__all__ = [
    "router",
]

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    description="Create user",
    response_model_exclude={"password"},
)
async def create_user(
    cmd: schemas.CreateUserCommand,
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    if not await auth_service.verify_captcha_in_redis(
        redis_pool=redis_pool,
        uid_captcha=cmd.uid_captcha,
        value_captcha=cmd.value_captcha,
    ):
        raise IncorrectCaptcha

    return await user_service.create_user(cmd=cmd)


@router.get(
    "/",
    response_model=List[schemas.User],
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Get all users without password field.",
)
async def read_all_users():
    return await user_service.read_all_users()


@router.get(
    "/{user_id:int}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Read specific user without password field.",
)
async def read_user(
    user_id: int = schemas.UserFields.id,
):
    return await user_service.read_specific_user_by_id(
        query=schemas.ReadUserByIdQuery(id=user_id),
    )


@router.get(
    "/{username:str}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Read specific user without password field.",
)
async def read_user(
    username: str = schemas.UserFields.username,
):
    return await user_service.read_specific_user_by_username(
        query=schemas.ReadUserByUserNameQuery(username=username),
    )


@router.patch(
    "/password",
    response_model=schemas.User,
    status_code=status.HTTP_202_ACCEPTED,
    description="Change password.",
    response_model_exclude={"password"},
)
async def change_password(
    cmd: schemas.ChangeUserPasswordCommand,
):
    return await user_service.change_password(cmd=cmd)


@router.delete(
    "/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Delete specific user",
)
async def delete_user(
    user_id: int = schemas.UserFields.id,
):
    return await user_service.delete_specific_user(
        cmd=schemas.DeleteUserCommand(id=user_id),
    )


@router.patch(
    "/user",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Update specific user without password field.",
)
async def update_user(
    cmd: schemas.UpdateUserCommand,
):
    return await user_service.update_specific_user_by_username(
        cmd=cmd,
    )


@router.post(
    "/notification",
    response_model=List[schemas.Notification],
    status_code=status.HTTP_200_OK,
    description="Receiving notifications by the user.",
)
async def get_notification(
    query: schemas.ReadNotificationQuery,
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    authorize.jwt_required()
    query = schemas.ReadNotificationWithUserUIDQuery(
        user_uid=authorize.get_raw_jwt()["uid"], view=query.view
    )
    return await notification_service.read_user_notifications(query=query)


@router.patch(
    "/notification",
    # response_model=List[schemas.Notification],
    status_code=status.HTTP_202_ACCEPTED,
    description="Mark notifications as read by the user.",
)
async def mark_as_read(
    query: schemas.MarkAsReadNotificationCommand,
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    authorize.jwt_required()
    query = schemas.MarkAsReadNotificationWithUserUIDCommand(
        user_uid=authorize.get_raw_jwt()["uid"],
        uid_notifications=query.uid_notifications,
    )
    return await notification_service.mark_as_read(query=query)
