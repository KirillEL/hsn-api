from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, root_validator, model_validator
from starlette import status
from fastapi import Request

from core.hsn.appointment import (
    HsnCommandAppointmentInitContext,
    hsn_command_appointment_initialize,
)
from .router import appointment_router
from api.exceptions import (
    ExceptionResponseSchema,
    ValidationException,
    DoctorNotAssignedException,
)


class AppointmentInitializeRequestBody(BaseModel):
    patient_id: int = Field(gt=0)
    date: Optional[str] = Field(None)
    date_next: Optional[str] = Field(None)

    @field_validator("date", "date_next")
    def check_date_format(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")

    @model_validator(mode="after")
    def check_dates(self):
        date = self.date
        date_next = self.date_next
        if date and date_next:
            date_dt = datetime.strptime(date, "%d.%m.%Y")
            date_next_dt = datetime.strptime(date_next, "%d.%m.%Y")

            if date_next_dt <= date_dt:
                raise ValidationException(
                    message="Дата следующего приема должна быть больше даты приема"
                )

        return self


@appointment_router.post(
    "/initialize",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Инициализация приема",
    status_code=status.HTTP_201_CREATED,
    tags=["Прием"],
)
async def appointment_initialize_route(
    request: Request, body: AppointmentInitializeRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentInitContext(
        user_id=request.user.id, doctor_id=request.user.doctor.id, **body.model_dump()
    )
    return await hsn_command_appointment_initialize(context)
