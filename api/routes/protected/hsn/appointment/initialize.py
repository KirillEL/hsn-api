from typing import Optional

from pydantic import BaseModel, Field
from starlette import status
from fastapi import Request

from core.hsn.appointment import HsnInitializeAppointmentContext, hsn_appointment_initialize
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema


class AppointmentInitializeRequestBody(BaseModel):
    patient_id: int = Field(gt=0)
    date_next: Optional[str] = Field(None)


@appointment_router.post(
    "/initialize",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Инициализация приема",
    status_code=status.HTTP_201_CREATED,
    tags=["Прием"]
)
async def appointment_initialize(request: Request, body: AppointmentInitializeRequestBody):
    context = HsnInitializeAppointmentContext(
        user_id=request.user.id,
        doctor_id=request.user.doctor.id,
        **body.model_dump()
    )
    return await hsn_appointment_initialize(context)