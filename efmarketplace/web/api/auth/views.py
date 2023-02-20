from datetime import timedelta
from typing import Optional, Dict, Union

from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from redis.asyncio import ConnectionPool
from pydantic import BaseModel

from efmarketplace import schemas
from efmarketplace.services import auth_service
from efmarketplace.services.redis.dependency import get_redis_pool
from efmarketplace.settings import settings
from efmarketplace.web.api.exceptions.auth import IncorrectCaptcha

router = APIRouter()

__all__ = [
    "router",
]


class SettingsAuthJWT(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET_KEY.get_secret_value()


access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRES)


@AuthJWT.load_config
def get_config() -> SettingsAuthJWT:
    return SettingsAuthJWT()


@router.post(
    "/login",
    response_model=schemas.Auth,
    status_code=status.HTTP_200_OK,
    description="Route for authorize.",
)
async def auth_user(
    cmd: schemas.AuthCommand,
    Authorize: AuthJWT = Depends(),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    if not await auth_service.verify_captcha_in_redis(
        redis_pool=redis_pool,
        uid_captcha=cmd.uid_captcha,
        value_captcha=cmd.value_captcha,
    ):
        raise IncorrectCaptcha

    user = await auth_service.check_user_password(cmd=cmd)

    access_token = Authorize.create_access_token(
        subject=user.username, expires_time=access_token_expires
    )
    refresh_token = Authorize.create_refresh_token(
        subject=user.username, expires_time=refresh_token_expires
    )
    return schemas.Auth(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh",
    response_model=schemas.Auth,
    description="Get new tokens pair.",
)
async def create_new_token_pair(
    Authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(
        subject=current_user, expires_time=access_token_expires
    )
    refresh_token = Authorize.create_refresh_token(
        subject=current_user, expires_time=refresh_token_expires
    )
    return schemas.Auth(access_token=access_token, refresh_token=refresh_token)


@router.get(
    "/me",
)
async def get_me(
    Authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> Optional[Dict[str, Union[str, int, bool]]]:
    Authorize.jwt_required()
    return Authorize.get_raw_jwt()


@router.post(
    "/captcha",
    response_model=schemas.CaptchaWithoutValue,
    status_code=status.HTTP_201_CREATED,
    description="Captcha.",
)
async def captcha(
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    return await auth_service.create_captcha(_cmd=schemas.CaptchaQuery(),
                                             redis_pool=redis_pool)
