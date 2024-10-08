from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update

from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from shared.db.db_session import db_session, SessionContext


class HsnCommandBlockComplaintUpdateContext(BaseModel):
    appointment_id: int
    has_fatigue: Optional[bool] = None
    has_dyspnea: Optional[bool] = None
    has_swelling_legs: Optional[bool] = None
    has_weakness: Optional[bool] = None
    has_orthopnea: Optional[bool] = None
    has_heartbeat: Optional[bool] = None
    note: Optional[str] = None


@SessionContext()
async def hsn_command_block_complaint_update(context: HsnCommandBlockComplaintUpdateContext):
    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query = (
        select(AppointmentDBModel.block_complaint_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor = await db_session.execute(query)
    block_complaint_id = cursor.scalar()
    if block_complaint_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_update = (
        update(AppointmentComplaintBlockDBModel)
        .values(**payload)
        .where(AppointmentComplaintBlockDBModel.id == block_complaint_id)
        .returning(AppointmentComplaintBlockDBModel)
    )
    cursor = await db_session.execute(query_update)
    await db_session.commit()
    updated_block_complaint = cursor.scalars().first()
    return AppointmentComplaintBlock.model_validate(updated_block_complaint)