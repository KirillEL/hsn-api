from typing import Optional

from .router import block_complaint_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock, hsn_command_appointment_block_complaint_create, \
    HsnCommandAppointmentBlockComplaintCreateContext
from pydantic import BaseModel, Field
from fastapi import Request


class CreateBlockComplaintRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    has_fatigue: bool = Field(False)
    has_dyspnea: bool = Field(False)
    has_swelling_legs: bool = Field(False)
    has_weakness: bool = Field(False)
    has_orthopnea: bool = Field(False)
    has_heartbeat: bool = Field(True)
    note: str = Field(None, max_length=1000, examples=["Your note here"], description="Optional note, can be omitted.")


@block_complaint_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_complaint(request: Request, body: CreateBlockComplaintRequestBody):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentBlockComplaintCreateContext(**body.model_dump())
    return await hsn_command_appointment_block_complaint_create(context)
