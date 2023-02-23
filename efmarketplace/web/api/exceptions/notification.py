from fastapi import status

from .base import BaseAPIException

__all__ = [
    "InvalidIDsInRequest",
]


class InvalidIDsInRequest(BaseAPIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    message = "You may have specified non-existent ids"
