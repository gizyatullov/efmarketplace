from fastapi import status

from .base import BaseAPIException

__all__ = [
    "NotFound",
    "AlreadyExists",
]


class NotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "object not found"


class AlreadyExists(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = "object already exists"
