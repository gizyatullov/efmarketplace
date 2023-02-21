from tortoise import Optional

from efmarketplace.db.models.user import User


async def check_auth() -> Optional[User]:
    return await User.filter(id=2).first()
