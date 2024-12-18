from typing import Optional

from fastapi import Request
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.complaint import (
    HsnCommandBlockComplaintUpdateContext,
    hsn_command_block_complaint_update,
)
from domains.core.hsn.appointment.blocks.complaint.model import (
    AppointmentComplaintBlockResponse,
)
from .router import block_complaint_router
from pydantic import BaseModel, Field


class UpdateBlockComplaintRequestBody(BaseModel):
    has_fatigue: Optional[bool] = Field(False)
    has_dyspnea: Optional[bool] = Field(False)
    increased_ad: Optional[bool] = Field(False)
    rapid_heartbeat: Optional[bool] = Field(False)
    has_swelling_legs: Optional[bool] = Field(False)
    has_weakness: Optional[bool] = Field(False)
    has_orthopnea: Optional[bool] = Field(False)
    heart_problems: Optional[bool] = Field(False)
    note: Optional[str] = Field(
        None,
        max_length=1000,
        examples=["Your note here"],
        description="Optional note, can be omitted.",
    )


@block_complaint_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentComplaintBlockResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_block_complaint_route(
    request: Request, appointment_id: int, body: UpdateBlockComplaintRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandBlockComplaintUpdateContext(
        appointment_id=appointment_id, **body.model_dump()
    )
    doctor_id: int = request.user.doctor.id
    return await hsn_command_block_complaint_update(doctor_id, context)
