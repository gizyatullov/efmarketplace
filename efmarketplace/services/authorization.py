from typing import List, Optional, Type

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from efmarketplace import schemas
from efmarketplace.db.dao.user import UserDAO
from efmarketplace.web.api.exceptions.auth import NotEnoughRightsFor

__all__ = [
    "Auth",
    "auth_only_admin",
    "auth_only",
]


class Auth:
    def __init__(
        self,
        allowed_roles: Optional[List[str]] = None,
        user_repository: Optional[Type[UserDAO]] = None,
        allowed_groups: Optional[List[str]] = None,
    ):
        self.allowed_roles = allowed_roles
        self.allowed_groups = allowed_groups
        self.repository = user_repository

    async def __call__(self, authorize: AuthJWT = Depends()) -> Optional[AuthJWT]:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        if not (self.allowed_roles and self.repository):
            return

        u = await self.repository.read_by_username_select_fields(
            username=username, fields=["role_name"]
        )
        role_name = u.role_name.value
        if role_name not in self.allowed_roles:
            raise NotEnoughRightsFor(
                message=f"Insufficient rights for the role {role_name}"
            )

        return authorize


auth_only_admin = Auth(
    allowed_roles=[schemas.UserRole.ADMIN.value], user_repository=UserDAO
)

auth_only = Auth()
