from efmarketplace.db.models.user import User
from tortoise import Optional


async def check_auth() -> Optional[User]:
    return await User.filter(id=2).first()
