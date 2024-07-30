from core.hsn.appointment.blocks.purpose import (
    HsnAppointmentPurposeUpdateContext,
    hsn_appointment_purpose_update,
    AppointmentPurposeFlat,
)
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Request


class UpdateBlockPurposeRequestBody(BaseModel):
    medicine_prescription_id: Optional[int] = Field(None, gt=0)
    dosa: Optional[str] = Field(None, max_length=100)
    note: Optional[str] = Field(None)


@block_purpose_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentPurposeFlat,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_block_purpose(
    request: Request, appointment_id: int, body: UpdateBlockPurposeRequestBody
):
    context = HsnAppointmentPurposeUpdateContext(
        user_id=request.user.id, appointment_id=appointment_id, **body.model_dump()
    )
    return await hsn_appointment_purpose_update(context)
