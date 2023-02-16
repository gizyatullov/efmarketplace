from fastapi import status

from .base import BaseAPIException

__all__ = [
    'IncorrectLengthFingerprint',
    'IncorrectUsernameOrPassword',
    'IncorrectCaptcha',
]


class IncorrectLengthFingerprint(BaseAPIException):
    status_code = 400
    message = 'Incorrect fingerprint'


class IncorrectUsernameOrPassword(BaseAPIException):
    status_code = 406
    message = 'Incorrect username or password or secret key'


class IncorrectCaptcha(BaseAPIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    message = 'Incorrect value captcha or timeout has expired.'
