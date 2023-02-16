from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field, PositiveInt, AnyHttpUrl

from .base import BaseModel

__all__ = [
    'User',
    'UserFields',
    'CreateUserCommand',
    'ReadUserByIdQuery',
    'ReadUserByUserNameQuery',
    'UpdateUserCommand',
    'DeleteUserCommand',
    'ChangeUserPasswordCommand',
    'UserRole',
]


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'


class UserFields:
    id = Field(description='User id.', example=2)
    username = Field(description='User Login', example='TestTest')
    password = Field(
        description='User password',
        example='strong password',
        min_length=6,
        max_length=256,
    )
    old_password = Field(
        description='Old user password.',
        example='strong password',
        min_length=6,
        max_length=256,
    )
    new_password = Field(
        description='New user password.',
        example='strong password',
        min_length=6,
        max_length=256,
    )
    role_name = Field(
        description='User role.',
        example=UserRole.USER.value,
    )
    is_seller = Field(
        description='The seller ?',
        example=False,
        default=None,
    )
    btc_balance = Field(
        description='Quantity btc.',
        example=1051.0,
        default=None,
    )
    btc_address = Field(
        description='Address btc.',
        example='3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy',
        default=None,
    )
    otp = Field(
        description='?.',
        example='?',
        default=None,
    )
    city = Field(
        description='User\'s city',
        example='Ul`yanovsk',
        default=None,
    )
    avatar = Field(
        description='URI photo user.',
        example='https://img.desktopwallpapers.ru/animals/pics/wide/1920x1200/6369fc18cca723f6a53f8730d420e7ee.jpg',
        default=None,
    )
    is_banned = Field(
        description='Banned ?',
        example=False,
        default=None,
    )
    user_ban_date = Field(
        description='If banned, until what time ?',
        example='2023-09-21 12:00:00',
        default=None,
    )
    created = Field(
        description='When the user registered ?',
        example='2022-09-21 12:00:00',
    )
    uid_captcha = Field(
        description='Unique ID captcha',
        example='d22dee4f-44af-4b25-831a-5ba7bc75bca4',
    )
    value_captcha = Field(
        description='Value captcha',
        example='51iu6v',
    )


class BaseUser(BaseModel):
    """Base model for user."""

    class Config:
        orm_mode = True


class User(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: str = UserFields.password
    role_name: UserRole = UserFields.role_name
    is_seller: bool = UserFields.is_seller
    btc_balance: Optional[float] = UserFields.btc_balance
    btc_address: Optional[str] = UserFields.btc_address
    otp: Optional[str] = UserFields.otp
    city: Optional[str] = UserFields.city
    avatar: Optional[AnyHttpUrl] = UserFields.avatar
    created: datetime = UserFields.created
    is_banned: Optional[bool] = UserFields.is_banned
    user_ban_date: Optional[datetime] = UserFields.user_ban_date


# Commands.
class CreateUserCommand(BaseUser):
    username: str = UserFields.username
    password: str = UserFields.password
    role_name: UserRole = UserFields.role_name
    uid_captcha: str = UserFields.uid_captcha
    value_captcha: str = UserFields.value_captcha


class UpdateUserCommand(BaseUser):
    username: str = UserFields.username
    role_name: Optional[UserRole] = UserFields.role_name
    is_seller: bool = UserFields.is_seller
    btc_balance: float = UserFields.btc_balance
    btc_address: str = UserFields.btc_address
    otp: str = UserFields.otp
    city: str = UserFields.city
    avatar: AnyHttpUrl = UserFields.avatar
    is_banned: bool = UserFields.is_banned
    user_ban_date: datetime = UserFields.user_ban_date


class DeleteUserCommand(BaseUser):
    id: PositiveInt = UserFields.id


class ChangeUserPasswordCommand(BaseUser):
    id: PositiveInt = UserFields.id
    old_password: str = UserFields.old_password
    new_password: str = UserFields.new_password


# Query
class ReadUserByUserNameQuery(BaseUser):
    username: str = UserFields.username


class ReadUserByIdQuery(BaseUser):
    id: PositiveInt = UserFields.id
