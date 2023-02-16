from fastapi import status

from .base import BaseAPIException

__all__ = ['UserAlreadyExist',
           'IncorrectOldPassword',
           'IncorrectPasswordLength', ]


class UserAlreadyExist(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = 'User already exist.'


class IncorrectPasswordLength(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Incorrect password length'


class IncorrectOldPassword(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Incorrect old password.'
