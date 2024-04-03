from pydantic import BaseModel, Field
from sqlalchemy import insert

from .router import admin_appointment_block_complaint_router
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema
from fastapi import Request

class CreateAppointmentBlockComplaintRequestBody(BaseModel):
    has_fatigue: bool = Field(False)
    has_dyspnea: bool = Field(False)
    has_swelling_legs: bool = Field(False)
    has_weakness: bool = Field(False)
    has_orthopnea: bool = Field(False)
    has_heartbeat: bool = Field(True)
    note: str = Field(None, max_length=1000, examples=["Your note here"], description="Optional note, can be omitted.")

@admin_appointment_block_complaint_router.post(
    "/block/complaint/create",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_appointment_block_complaint_create(request: Request, body: CreateAppointmentBlockComplaintRequestBody):
    try:
        query = (
            insert(AppointmentComplaintBlockDBModel)
            .values(**body.model_dump())
        )
        await db_session.execute(query)
        await db_session.commit()
        return True
    except Exception as e:
        await db_session.rollback()
        raise e
