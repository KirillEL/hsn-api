from datetime import date as tdate, datetime

from loguru import logger
from sqlalchemy import insert, update, exc, Result, Update
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningInsert

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException, ForbiddenException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from pydantic import BaseModel
from typing import Optional

from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from shared.db.queries import db_query_entity_by_id


class HsnCommandAppointmentBlockLaboratoryTestCreateContext(BaseModel):
    appointment_id: int

    nt_pro_bnp: Optional[float] = None
    nt_pro_bnp_date: Optional[str] = None
    hbalc: Optional[float] = None
    hbalc_date: Optional[str] = None

    eritrocit: Optional[float] = None
    hemoglobin: Optional[float] = None
    oak_date: Optional[str] = None

    tg: Optional[float] = None
    lpvp: Optional[float] = None
    lpnp: Optional[float] = None
    general_hc: Optional[float] = None
    natriy: Optional[float] = None
    kaliy: Optional[float] = None
    glukoza: Optional[float] = None
    mochevaya_kislota: Optional[float] = None
    skf: Optional[float] = None
    kreatinin: Optional[float] = None
    bk_date: Optional[str] = None

    protein: Optional[float] = None
    urine_eritrocit: Optional[float] = None
    urine_leycocit: Optional[float] = None
    microalbumuria: Optional[float] = None
    am_date: Optional[str] = None
    note: Optional[str] = None


@SessionContext()
async def hsn_command_appointment_block_laboratory_test_create(
        doctor_id: int,
        context: HsnCommandAppointmentBlockLaboratoryTestCreateContext
) -> int:
    appointment: AppointmentDBModel = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException(
            message="Прием c id:{} не найден".format(context.appointment_id)
        )

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(context.appointment_id))

    payload = context.model_dump(exclude={'appointment_id'})
    query: ReturningInsert = (
        insert(AppointmentLaboratoryTestBlockDBModel)
        .values(**payload)
        .returning(AppointmentLaboratoryTestBlockDBModel.id)
    )
    cursor: Result = await db_session.execute(query)
    new_block_laboratory_test_id: int = cursor.scalar()

    query_update_appointment: Update = (
        update(AppointmentDBModel)
        .values(
            block_laboratory_test_id=new_block_laboratory_test_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)
    await db_session.commit()

    return new_block_laboratory_test_id
