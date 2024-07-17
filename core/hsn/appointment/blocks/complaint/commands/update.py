from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from shared.db import Transaction
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from shared.db.db_session import session
from shared.db.transaction import Propagation


class HsnBlockComplaintUpdateContext(BaseModel):
    appointment_id: int
    has_fatigue: Optional[bool] = None
    has_dyspnea: Optional[bool] = None
    has_swelling_legs: Optional[bool] = None
    has_weakness: Optional[bool] = None
    has_orthopnea: Optional[bool] = None
    has_heartbeat: Optional[bool] = None
    note: Optional[str] = None


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_block_complaint_update(context: HsnBlockComplaintUpdateContext):
    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query = (
        select(AppointmentDBModel.block_complaint_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor = await session.execute(query)
    block_complaint_id = cursor.scalar()
    if block_complaint_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_update = (
        update(AppointmentComplaintBlockDBModel)
        .values(**payload)
        .where(AppointmentComplaintBlockDBModel.id == block_complaint_id)
        .returning(AppointmentComplaintBlockDBModel)
    )
    cursor = await session.execute(query_update)
    updated_block_complaint = cursor.scalars().first()
    return AppointmentComplaintBlock.model_validate(updated_block_complaint)