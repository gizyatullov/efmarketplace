from fastapi import status

from .base import BaseAPIException

__all__ = [
    "NotFoundTicket",
]


class NotFoundTicket(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Ticket with this ID does not exist"
