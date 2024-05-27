from typing import Optional

from core.hsn.appointment.model import PatientAppointmentFlat
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment import Appointment, HsnAppointmentListContext, hsn_appointment_list
from fastapi import Request, Depends
from pydantic import BaseModel


class GetAppointmentListQueryParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None

class GetOwnPatientAppointmentsResponse(BaseModel):
    data: list[PatientAppointmentFlat]
    total: int

@appointment_router.get(
    "",
    response_model=GetOwnPatientAppointmentsResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    tags=["Прием"],
    summary="Получить список всех приемов"
)
async def get_appointment_list(request: Request, params: GetAppointmentListQueryParams = Depends()):
    context = HsnAppointmentListContext(
        user_id=request.user.doctor.id,
        **params.dict()
    )
    return await hsn_appointment_list(context)
