from typing import Optional, Union

from efmarketplace.pkg.types.strings import NotEmptyStr
from fastapi import HTTPException
from starlette import status

__all__ = ["BaseAPIException"]


class BaseAPIException(HTTPException):
    message: Optional[Union[NotEmptyStr, str]] = "Base API Exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: Optional[NotEmptyStr] = None):
        if message is not None:
            self.message = message

        super().__init__(status_code=self.status_code, detail=self.message)
