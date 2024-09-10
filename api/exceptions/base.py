from datetime import datetime

from pydantic import BaseModel
from http import HTTPStatus

from sqlalchemy import exc


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
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = "user not found!"


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class UnauthorizedAdminException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = "you are not admin!"


class BadRequestException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class ValidationException(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class InternalServerException(CustomException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = "Ошибка сервера!"


class UnprocessableEntityException(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class BlockAlreadyExistsException(CustomException):
    code = HTTPStatus.CONFLICT
    error_code = HTTPStatus.CONFLICT
    message = ""


class DoctorNotAssignedException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = "Пользователю не назначен врач"


class AppointmentNotBelongsToUserException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = "Прием вам не принадлежит"


class MedicinePrescriptionCreateException(CustomException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = "Не удалось создать лекарственное назначение"


class ValidationErrorTelegramSendMessageModel:
    def __init__(
            self,
            message: str,
            doctor_id: int,
            doctor_name: str,
            doctor_last_name: str,
            date: str,
            description: str | exc.SQLAlchemyError
    ):
        self.message = message
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.doctor_last_name = doctor_last_name
        self.date = date
        self.description = description

    def __str__(self):
        error_message = (
            f"{self.message}\n"
            f"Врач: *{self.doctor_name} {self.doctor_last_name}*\n"
            f"ID врача: {self.doctor_id}\n"
            f"Дата и время: {self.date}\n\n"
            f"Описание ошибки: `{str(self.description)}`"
        )
        return error_message
