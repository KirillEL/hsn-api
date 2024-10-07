from typing import Optional

from pydantic import BaseModel

from core.hsn.appointment.model import PatientAppointmentFlat
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from fastapi import Request, Depends


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
async def get_appointment_list_route(request: Request, params: GetAppointmentListQueryParams = Depends()):
    if not request.user.doctor:
        raise DoctorNotAssignedException
    from core.hsn.appointment import HsnAppointmentListContext, hsn_appointment_list

    context = HsnAppointmentListContext(
        doctor_id=request.user.doctor.id,
        **params.model_dump()
    )
    return await hsn_appointment_list(request, context)
