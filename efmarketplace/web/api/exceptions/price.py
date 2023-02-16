from fastapi import status

from .base import BaseAPIException

__all__ = [
    'ServiceIsUnavailable',
]


class ServiceIsUnavailable(BaseAPIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    message = 'Service is temporarily unavailable'
