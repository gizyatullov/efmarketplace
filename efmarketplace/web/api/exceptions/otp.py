from fastapi import status

from .base import BaseAPIException

__all__ = [
    "OTPAlreadyInstalled",
]


class OTPAlreadyInstalled(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = "OTP already installed, try to update"
