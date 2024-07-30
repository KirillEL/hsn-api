from typing import Optional

from sqlalchemy import insert, update, exc

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import (
    check_appointment_exists,
)
from shared.db import Transaction
from shared.db.db_session import session
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import (
    AppointmentComplaintBlockDBModel,
)
from pydantic import BaseModel

from shared.db.transaction import Propagation


class HsnAppointmentBlockComplaintCreateContext(BaseModel):
    appointment_id: int
    has_fatigue: Optional[bool] = False
    has_dyspnea: Optional[bool] = False
    has_swelling_legs: Optional[bool] = False
    has_weakness: Optional[bool] = False
    has_orthopnea: Optional[bool] = False
    has_heartbeat: Optional[bool] = True
    note: Optional[str] = False


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_appointment_block_complaint_create(
    context: HsnAppointmentBlockComplaintCreateContext,
) -> int:
    await check_appointment_exists(context.appointment_id)
    payload = context.model_dump(exclude={"appointment_id"})
    query = (
        insert(AppointmentComplaintBlockDBModel)
        .values(**payload)
        .returning(AppointmentComplaintBlockDBModel.id)
    )
    cursor = await session.execute(query)
    new_complaint_block_id = cursor.scalar()

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(block_complaint_id=new_complaint_block_id)
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await session.execute(query_update_appointment)

    return new_complaint_block_id
