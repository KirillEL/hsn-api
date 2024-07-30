from typing import Optional

from fastapi import Request
from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.complaint import (
    AppointmentComplaintBlock,
    HsnBlockComplaintUpdateContext,
    hsn_block_complaint_update,
)
from core.hsn.appointment.blocks.complaint.model import AppointmentComplaintBlockResponse
from .router import block_complaint_router
from pydantic import BaseModel, Field


class UpdateBlockComplaintRequest(BaseModel):
    has_fatigue: Optional[bool] = Field(False)
    has_dyspnea: Optional[bool] = Field(False)
    has_swelling_legs: Optional[bool] = Field(False)
    has_weakness: Optional[bool] = Field(False)
    has_orthopnea: Optional[bool] = Field(False)
    has_heartbeat: Optional[bool] = Field(True)
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
async def update_block_complaint(
    appointment_id: int, body: UpdateBlockComplaintRequest
):
    context = HsnBlockComplaintUpdateContext(
        appointment_id=appointment_id, **body.model_dump()
    )
    return await hsn_block_complaint_update(context)
