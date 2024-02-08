from pydantic import BaseModel
from http import HTTPStatus


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class ExceptionResponseSchema(BaseModel):
    error: str


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class UserNotFoundException(CustomException):
    code = 404
    error_code = "USER__NOT__FOUND"
    message = "user not found!"


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description