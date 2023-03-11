from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field, PositiveInt

from efmarketplace.pkg.types.integeres import PositiveIntWithZero

from .base import BaseModel
from .general import ForPaginationFields

__all__ = [
    "User",
    "UserFields",
    "UsersWithPagination",
    "CreateUserCommand",
    "ReadAllUserQuery",
    "ReadUserByIdQuery",
    "ReadUserByUserNameQuery",
    "UpdateUserCommand",
    "DeleteUserCommand",
    "ChangeUserPasswordCommand",
    "ChangeUserPasswordWithIDCommand",
    "UserRole",
    "UserName",
    "UserIDMixin",
]


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserFields:
    id = Field(description="User id.", example=2)
    ids = Field(description="User ids.", example=[2, 4, 50])
    username = Field(description="User Login", example="good")
    password = Field(
        description="User password",
        example="password",
        min_length=6,
        max_length=256,
    )
    old_password = Field(
        description="Old user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    new_password = Field(
        description="New user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    role_name = Field(
        description="User role.",
        example=UserRole.USER.value,
    )
    is_seller = Field(
        description="The seller ?",
        example=False,
        default=None,
    )
    btc_balance = Field(
        description="Quantity btc.",
        example=1051.0,
        default=None,
    )
    btc_address = Field(
        description="Address btc.",
        example="3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
        default=None,
    )
    otp = Field(
        description="?.",
        example="?",
        default=None,
    )
    city = Field(
        description="User's city",
        example="Ul`yanovsk",
        default=None,
    )
    avatar = Field(
        description="URI photo user.",
        example="https://img.desktopwallpapers.ru/animals/pics/wide/1920x1200/6369fc18cca723f6a53f8730d420e7ee.jpg",
        default=None,
    )
    is_banned = Field(
        description="Banned ?",
        example=False,
        default=None,
    )
    user_ban_date = Field(
        description="If banned, until what time ?",
        example="2023-09-21 12:00:00",
        default=None,
    )
    created = Field(
        description="When the user registered ?",
        example="2022-09-21 12:00:00",
    )
    uid_captcha = Field(
        description="Unique ID captcha",
        example="d22dee4f-44af-4b25-831a-5ba7bc75bca4",
    )
    value_captcha = Field(
        description="Value captcha",
        example="51iu6v9s",
    )


class BaseUser(BaseModel):
    """Base model for user."""

    class Config:
        orm_mode = True


class User(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    role_name: UserRole = UserFields.role_name
    is_seller: bool = UserFields.is_seller
    btc_balance: Optional[float] = UserFields.btc_balance
    btc_address: Optional[str] = UserFields.btc_address
    city: Optional[str] = UserFields.city
    avatar: Optional[str] = UserFields.avatar
    created: datetime = UserFields.created
    is_banned: Optional[bool] = UserFields.is_banned
    user_ban_date: Optional[datetime] = UserFields.user_ban_date


class UsersWithPagination(BaseUser):
    items: List[User]
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


class UserName(BaseUser):
    username: str = UserFields.username


class UserIDMixin(BaseUser):
    user_id: PositiveInt = UserFields.id


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
    btc_address: str = UserFields.btc_address
    city: str = UserFields.city
    avatar: str = UserFields.avatar
    is_banned: bool = UserFields.is_banned
    user_ban_date: datetime = UserFields.user_ban_date


class DeleteUserCommand(BaseUser):
    id: PositiveInt = UserFields.id


class ChangeUserPasswordCommand(BaseUser):
    old_password: str = UserFields.old_password
    new_password: str = UserFields.new_password


class ChangeUserPasswordWithIDCommand(ChangeUserPasswordCommand):
    id: PositiveInt = UserFields.id


# Query
class ReadAllUserQuery(BaseUser):
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0


class ReadUserByUserNameQuery(BaseUser):
    username: str = UserFields.username


class ReadUserByIdQuery(BaseUser):
    id: PositiveInt = UserFields.id
