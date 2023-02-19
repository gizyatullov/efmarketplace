from functools import wraps

from efmarketplace.web.api.users.controler import check_auth
from fastapi import HTTPException


def auth_required(func):  # type: ignore
    @wraps(func)
    async def wrapper(*args, **kwargs):  # type: ignore
        user = await check_auth()
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return await func(*args, **kwargs)

    return wrapper
