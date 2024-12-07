from typing import Optional

from pydantic import BaseModel

from domains.core.hsn.appointment.model import AppointmentsListDto
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from fastapi import Request, Depends


class GetAppointmentListQueryParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None


class GetOwnPatientAppointmentsResponse(BaseModel):
    data: list[AppointmentsListDto]
    total: int


@appointment_router.get(
    "",
    response_model=GetOwnPatientAppointmentsResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    tags=["Прием"],
    summary="Получить список всех приемов",
)
async def get_appointment_list_route(
    request: Request, params: GetAppointmentListQueryParams = Depends()
):
    if not request.user.doctor:
        raise DoctorNotAssignedException
    from domains.core.hsn.appointment import (
        HsnAppointmentListContext,
        hsn_query_appointment_list,
    )

    context = HsnAppointmentListContext(
        doctor_id=request.user.doctor.id, **params.model_dump()
    )
    return await hsn_query_appointment_list(request, context)
