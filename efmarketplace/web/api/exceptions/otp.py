from fastapi import status

from .base import BaseAPIException

__all__ = [
    "OTPAlreadyInstalled",
    "OTPIncorrect",
]


class OTPAlreadyInstalled(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = "OTP already installed, try to remove, then install"


class OTPIncorrect(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Incorrect OTP code"
