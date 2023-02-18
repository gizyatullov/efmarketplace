from datetime import timedelta

from fastapi import APIRouter, status, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from redis.asyncio import ConnectionPool

from efmarketplace import schemas
from efmarketplace.services import auth_service
from efmarketplace.settings import settings
from efmarketplace.services.redis.dependency import get_redis_pool
from efmarketplace.web.api.exceptions.auth import IncorrectCaptcha

router = APIRouter()

__all__ = [
    'router',
]

access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRES)


@AuthJWT.load_config
def get_config():
    return settings


@router.post(
    '/login',
    response_model=schemas.Auth,
    status_code=status.HTTP_200_OK,
    description='Route for authorize.',
)
async def auth_user(
    cmd: schemas.AuthCommand,
    authorize: AuthJWT = Depends(),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    # if not await auth_service.verify_captcha_in_redis(redis_pool=redis_pool,
    #                                                   uid_captcha=cmd.uid_captcha,
    #                                                   value_captcha=cmd.value_captcha):
    #     raise IncorrectCaptcha

    user = await auth_service.check_user_password(cmd=cmd)

    access_token = authorize.create_access_token(subject=user.username,
                                                 expires_time=access_token_expires)
    refresh_token = authorize.create_refresh_token(subject=user.username,
                                                   expires_time=refresh_token_expires)
    return schemas.Auth(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    '/refresh',
    response_model=schemas.Auth,
    description='Get new tokens pair.',
)
async def create_new_token_pair(
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(subject=current_user,
                                                 expires_time=access_token_expires)
    refresh_token = authorize.create_refresh_token(subject=current_user,
                                                   expires_time=refresh_token_expires)
    return schemas.Auth(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get(
    '/me',
)
async def get_me(
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    authorize.jwt_required()
    return authorize.get_raw_jwt()


@router.post(
    '/captcha',
    response_model=schemas.CaptchaWithoutValue,
    status_code=status.HTTP_201_CREATED,
    description='Captcha.',
)
async def captcha(
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    return await auth_service.create_captcha(cmd=schemas.CaptchaQuery(),
                                             redis_pool=redis_pool)
