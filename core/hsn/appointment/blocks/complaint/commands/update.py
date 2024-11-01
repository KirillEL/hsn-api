from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update, Select, Result
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from shared.db.db_session import db_session, SessionContext


class HsnCommandBlockComplaintUpdateContext(BaseModel):
    appointment_id: int
    has_fatigue: Optional[bool] = None
    has_dyspnea: Optional[bool] = None
    increased_ad: Optional[bool] = None
    rapid_heartbeat: Optional[bool] = None
    has_swelling_legs: Optional[bool] = None
    has_weakness: Optional[bool] = None
    has_orthopnea: Optional[bool] = None
    note: Optional[str] = None


@SessionContext()
async def hsn_command_block_complaint_update(
        context: HsnCommandBlockComplaintUpdateContext
) -> AppointmentComplaintBlock:
    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query: Select = (
        select(AppointmentDBModel.block_complaint_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_complaint_id: int = cursor.scalar()
    if not block_complaint_id:
        raise NotFoundException(message="У приема нет данного блока!")

    query_update: ReturningUpdate = (
        update(AppointmentComplaintBlockDBModel)
        .values(**payload)
        .where(AppointmentComplaintBlockDBModel.id == block_complaint_id)
        .returning(AppointmentComplaintBlockDBModel)
    )
    cursor: Result = await db_session.execute(query_update)
    await db_session.commit()
    updated_block_complaint = cursor.scalars().first()
    return AppointmentComplaintBlock.model_validate(updated_block_complaint)
