import base64
import io
from typing import Type

import pyotp
import qrcode

from efmarketplace import schemas
from efmarketplace.db.dao.user import UserDAO
from efmarketplace.web.api import exceptions

__all__ = ["UserService"]


class UserService:
    repository: Type[UserDAO]

    def __init__(self, user_repository: Type[UserDAO]):
        self.repository = user_repository

    async def create_user(self, cmd: schemas.CreateUserCommand) -> schemas.User:
        return await self.repository.create(cmd=cmd)

    async def read_all_users(
        self, query: schemas.ReadAllUserQuery
    ) -> schemas.UsersWithPagination:
        return await self.repository.read_all(query=query)

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

    async def set_otp(self, cmd: schemas.SetOTPWithUserNameCommand) -> schemas.OTP:
        if await self.repository.check_otp_install(username=cmd.username):
            raise exceptions.OTPAlreadyInstalled

        k = await self.repository.set_otp(username=cmd.username)
        totp = pyotp.totp.TOTP(s=k).provisioning_uri(
            name="efmarketplace", issuer_name=cmd.username
        )
        qr = qrcode.make(totp)
        buffer = io.BytesIO()
        qr.save(buffer)
        buffer.seek(0)
        qr = buffer.read()
        qr = base64.b64encode(s=qr).decode(encoding="utf-8")

        return schemas.OTP(otp=k, qr=qr)
