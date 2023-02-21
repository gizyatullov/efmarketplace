from pydantic import UUID4, Field

from efmarketplace.pkg.types import NotEmptySecretStr
from efmarketplace.schemas.user import UserFields

from .base import BaseModel

__all__ = [
    "Auth",
    "AuthCommand",
    "LogoutCommand",
    "CaptchaQuery",
    "Captcha",
    "CaptchaWithoutValue",
]


class AuthFields:
    access_token = Field(description="Bearer access token", example="exam.ple.token")
    refresh_token = Field(description="Bearer refresh token", example="exam.ple.token")
    fingerprint = Field(
        description="Unique fingerprint of user device",
        example="u-u-i-d",
    )
    role_name = UserFields.role_name
    username = UserFields.username
    password = UserFields.password
    uid_captcha = UserFields.uid_captcha
    value_captcha = UserFields.value_captcha


class BaseAuth(BaseModel):
    """Base model for auth."""


class Auth(BaseAuth):
    access_token: NotEmptySecretStr = AuthFields.access_token
    refresh_token: NotEmptySecretStr = AuthFields.refresh_token


class AuthCommand(BaseAuth):
    username: str = AuthFields.username
    password: str = AuthFields.password
    uid_captcha: str = AuthFields.uid_captcha
    value_captcha: str = AuthFields.value_captcha


class LogoutCommand(BaseAuth):
    username: str = AuthFields.username
    refresh_token: NotEmptySecretStr = AuthFields.refresh_token


class BaseCaptcha(BaseModel):
    """Base model for captcha."""


class Captcha(BaseModel):
    uid: UUID4
    image: str
    value: str


class CaptchaWithoutValue(BaseModel):
    uid: UUID4
    image: str


# Query
class CaptchaQuery(BaseCaptcha):
    ...
