from fastapi import status

from .base import BaseAPIException

__all__ = [
    "NotFound",
]


class NotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "object not found"
