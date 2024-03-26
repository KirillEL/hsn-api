from typing import Optional

from sqlalchemy import insert

from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from pydantic import BaseModel


class HsnAppointmentBlockComplaintCreateContext(BaseModel):
    has_fatigue: Optional[bool] = False
    has_dyspnea: Optional[bool] = False
    has_swelling_legs: Optional[bool] = False
    has_weakness: Optional[bool] = False
    has_orthopnea: Optional[bool] = False
    has_heartbeat: Optional[bool] = True
    note: Optional[str] = False


@SessionContext()
async def hsn_appointment_block_complaint_create(context: HsnAppointmentBlockComplaintCreateContext) -> int:
    query = (
        insert(AppointmentComplaintBlockDBModel)
        .values(**context.model_dump())
        .returning(AppointmentComplaintBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_complaint_block_id = cursor.scalar()

    return new_complaint_block_id
