import datetime
from typing import List, Literal, Union, overload

from efmarketplace import schemas
from efmarketplace.db import models
from efmarketplace.schemas import (
    ChangeUserPasswordWithIDCommand,
    CreateUserCommand,
    DeleteUserCommand,
    ReadUserByIdQuery,
    ReadUserByUserNameQuery,
    UpdateUserCommand,
)
from efmarketplace.web.api import exceptions
from efmarketplace.web.api.exceptions.user import IncorrectOldPassword

from .base import BaseDAO

__all__ = ["UserDAO"]

Model = models.User
Schema = schemas.User


class UserDAO(BaseDAO[Model]):
    _model = Model

    @staticmethod
    async def create(cmd: CreateUserCommand) -> Schema:
        if Model.exists(username=cmd.username):
            raise exceptions.AlreadyExists(message="login busy")
        u = Model(
            username=cmd.username,
            role_name=cmd.role_name,
        )
        await u.set_password(password=cmd.password)
        await u.save()
        return Schema.from_orm(u)

    @staticmethod
    @overload
    async def read(query: ReadUserByIdQuery, orm_obj: Literal[True]) -> Model:
        ...

    @staticmethod
    @overload
    async def read(query: ReadUserByIdQuery, orm_obj: Literal[False]) -> Schema:
        ...

    @staticmethod
    async def read(
        query: ReadUserByIdQuery, orm_obj: bool = False
    ) -> Union[Schema, Model]:
        u = await Model.get(id=query.id)
        if orm_obj:
            return u
        return Schema.from_orm(u)

    @staticmethod
    @overload
    async def read_by_username(
        query: ReadUserByUserNameQuery, orm_obj: Literal[True]
    ) -> Model:
        ...

    @staticmethod
    @overload
    async def read_by_username(
        query: ReadUserByUserNameQuery, orm_obj: Literal[False]
    ) -> Schema:
        ...

    @staticmethod
    async def read_by_username(
        query: ReadUserByUserNameQuery, orm_obj: bool = False
    ) -> Union[Schema, Model]:
        u = await Model.get(username=query.username)
        return u if orm_obj else Schema.from_orm(u)

    @staticmethod
    async def read_by_username_select_fields(username: str, fields: List[str]) -> Model:
        u = await Model.get(username=username).only(*fields)
        return u

    @staticmethod
    async def read_all(query: schemas.ReadAllUserQuery) -> schemas.UsersWithPagination:
        u = (
            await Model.all()
            .limit(query.limit)
            .filter(id__gt=query.limit * query.offset)
            .order_by("id")
        )
        total = await Model.all().count()
        result = [Schema.from_orm(item) for item in u]
        return schemas.UsersWithPagination(
            items=result, total=total, page=query.offset, size=query.limit
        )

    @staticmethod
    async def delete(cmd: DeleteUserCommand) -> Schema:
        u = await Model.get(id=cmd.id)
        result = Schema.from_orm(u)
        await u.delete()
        return result

    @classmethod
    async def change_password(cls, cmd: ChangeUserPasswordWithIDCommand) -> Schema:
        u = await cls.read(query=ReadUserByIdQuery(id=cmd.id), orm_obj=True)
        if not u or not await u.check_password(password=cmd.old_password):
            raise IncorrectOldPassword
        await u.set_password(password=cmd.new_password)
        await u.save()
        return Schema.from_orm(obj=u)

    @classmethod
    async def update_specific_user_by_username(cls, cmd: UpdateUserCommand) -> Schema:
        u = await cls.read_by_username(
            query=ReadUserByUserNameQuery(username=cmd.username), orm_obj=True
        )

        for k, v in cmd.dict(exclude={"username"}, exclude_none=True).items():
            if k in ("user_ban_date",):
                v = datetime.datetime.fromisoformat(v)
            setattr(u, k, v)

        await u.save()

        return Schema.from_orm(obj=u)

    @classmethod
    async def check_otp_install(cls, username: str) -> bool:
        u = await cls.read_by_username_select_fields(username=username, fields=["otp"])
        return True if u.otp else False

    @classmethod
    async def set_otp(cls, username: str) -> str:
        u = await Model.get(username=username)
        k = await u.set_otp()
        await u.save()
        return k
