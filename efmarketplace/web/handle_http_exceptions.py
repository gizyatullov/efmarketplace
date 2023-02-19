"""handlers that handle internal error raise and returns ``http json``
response.

Examples:
    For example, if in some level in code you raise error inherited by
    BaseAPIException::

        ...  # exceptions.py
        class E(BaseAPIException):
            status_code = status.HTTP_200_OK
            message = "test error."

        ...  # some_file.py
        async def some_internal_function():
            raise E

    When `some_internal_function` called, exception will process by
    ``handle_api_exceptions`` and returns json object::

        {
            "message": "test error."
        }
"""
from efmarketplace.web.api.exceptions.base import BaseAPIException
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

__all__ = [
    "handle_internal_exception",
    "handle_api_exceptions",
    "authjwt_exception_handler",
]


def handle_api_exceptions(request: Request, exc: BaseAPIException) -> JSONResponse:
    """Handle all internal exceptions which inherited from
    `BaseAPIException`."""
    _ = request

    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


def handle_internal_exception(request: Request, exc: Exception) -> JSONResponse:
    """Handle all internal unhandled exceptions."""
    _ = request

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": repr(exc)},
    )


def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
