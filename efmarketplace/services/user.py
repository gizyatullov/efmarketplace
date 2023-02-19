from typing import List, Type

from efmarketplace import schemas
from efmarketplace.db.dao.user import UserDAO

__all__ = ["UserService"]


class UserService:
    repository: Type[UserDAO]

    def __init__(self, user_repository: Type[UserDAO]):
        self.repository = user_repository

    async def create_user(self, cmd: schemas.CreateUserCommand) -> schemas.User:
        return await self.repository.create(cmd=cmd)

    async def read_all_users(self) -> List[schemas.User]:
        return await self.repository.read_all()

    async def read_specific_user_by_username(
        self, query: schemas.ReadUserByUserNameQuery, orm_obj: bool = False
    ):
        return await self.repository.read_by_username(query=query, orm_obj=orm_obj)

    async def read_specific_user_by_id(
        self,
        query: schemas.ReadUserByIdQuery,
    ) -> schemas.User:
        return await self.repository.read(query=query)

    async def change_password(
        self,
        cmd: schemas.ChangeUserPasswordCommand,
    ) -> schemas.User:
        return await self.repository.change_password(cmd=cmd)

    async def delete_specific_user(
        self, cmd: schemas.DeleteUserCommand
    ) -> schemas.User:
        return await self.repository.delete(cmd=cmd)

    async def update_specific_user_by_username(
        self, cmd: schemas.UpdateUserCommand
    ) -> schemas.User:
        return await self.repository.update_specific_user_by_username(cmd=cmd)
