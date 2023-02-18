from typing import List, Union
import datetime

from tortoise import models

from .base import BaseDAO
from efmarketplace import schemas
from efmarketplace.db.models.user import User
from efmarketplace.web.api.exceptions.user import IncorrectOldPassword

__all__ = ['UserDAO']


class UserDAO(BaseDAO):
    def get_model(self) -> models.Model:
        return User

    async def create(self, cmd: schemas.CreateUserCommand) -> schemas.User:
        u = User(
            username=cmd.username,
            role_name=cmd.role_name,
        )
        await u.set_password(password=cmd.password)
        await u.save()
        return schemas.User.from_orm(u)

    async def read(self,
                   query: schemas.ReadUserByIdQuery,
                   orm_obj: bool = False) -> Union[schemas.User, User]:
        u = await User.get(id=query.id)
        if orm_obj:
            return u
        return schemas.User.from_orm(u)

    async def read_by_username(
        self,
        query: schemas.ReadUserByUserNameQuery,
        orm_obj: bool = False
    ) -> Union[schemas.User, User]:
        u = await User.get(username=query.username)
        if orm_obj:
            return u
        return schemas.User.from_orm(u)

    async def read_all(self) -> List[schemas.User]:
        u = await User.all()
        result = [schemas.User.from_orm(item) for item in u]
        return result

    async def delete(self, cmd: schemas.DeleteUserCommand) -> schemas.User:
        u = await User.get(id=cmd.id)
        result = schemas.User.from_orm(u)
        await u.delete()
        return result

    async def change_password(self,
                              cmd: schemas.ChangeUserPasswordCommand) -> schemas.User:
        u = await self.read(query=schemas.ReadUserByIdQuery(id=cmd.id), orm_obj=True)
        if not u or not await u.check_password(password=cmd.old_password):
            raise IncorrectOldPassword
        await u.set_password(password=cmd.new_password)
        await u.save()
        return schemas.User.from_orm(obj=u)

    async def update_specific_user_by_username(self,
                                               cmd: schemas.UpdateUserCommand) -> schemas.User:
        u = await self.read_by_username(
            query=schemas.ReadUserByUserNameQuery(username=cmd.username),
            orm_obj=True)

        for k, v in cmd.dict(exclude={'username'}, exclude_none=True).items():
            if k in ('user_ban_date',):
                v = datetime.datetime.fromisoformat(v)
            setattr(u, k, v)

        await u.save()

        return schemas.User.from_orm(obj=u)
