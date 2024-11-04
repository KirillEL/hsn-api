from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update, Select, Result
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.queries import db_query_entity_by_id


class HsnCommandBlockLaboratoryTestUpdateContext(BaseModel):
    appointment_id: int
    nt_pro_bnp: Optional[float] = None
    nt_pro_bnp_date: Optional[str] = None
    hbalc: Optional[float] = None
    hbalc_date: Optional[str] = None
    eritrocit: Optional[float] = None
    eritrocit_date: Optional[str] = None
    hemoglobin: Optional[float] = None
    hemoglobin_date: Optional[str] = None
    tg: Optional[float] = None
    tg_date: Optional[str] = None
    lpvp: Optional[float] = None
    lpvp_date: Optional[str] = None
    lpnp: Optional[float] = None
    lpnp_date: Optional[str] = None
    general_hc: Optional[float] = None
    general_hc_date: Optional[str] = None
    natriy: Optional[float] = None
    natriy_date: Optional[str] = None
    kaliy: Optional[float] = None
    kaliy_date: Optional[str] = None
    glukoza: Optional[float] = None
    glukoza_date: Optional[str] = None
    mochevaya_kislota: Optional[float] = None
    mochevaya_kislota_date: Optional[str] = None
    skf: Optional[float] = None
    skf_date: Optional[str] = None
    kreatinin: Optional[float] = None
    kreatinin_date: Optional[str] = None
    protein: Optional[float] = None
    protein_date: Optional[str] = None
    urine_eritrocit: Optional[float] = None
    urine_eritrocit_date: Optional[str] = None
    urine_leycocit: Optional[float] = None
    urine_leycocit_date: Optional[str] = None
    microalbumuria: Optional[float] = None
    microalbumuria_date: Optional[str] = None
    note: Optional[str] = None


@SessionContext()
async def hsn_command_block_laboratory_test_update(
        doctor_id: int,
        context: HsnCommandBlockLaboratoryTestUpdateContext
) -> AppointmentLaboratoryTestBlock:
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(context.appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(context.appointment_id))

    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query: Select = (
        select(AppointmentDBModel.block_laboratory_test_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )

    cursor: AsyncResult = await db_session.execute(query)

    block_laboratory_test_id: int = cursor.scalar()
    if not block_laboratory_test_id:
        raise NotFoundException(message="У приема с id:{} нет данного блока".format(context.appointment_id))

    query_update: ReturningUpdate = (
        update(AppointmentLaboratoryTestBlockDBModel)
        .values(**payload)
        .where(AppointmentLaboratoryTestBlockDBModel.id == block_laboratory_test_id)
        .returning(AppointmentLaboratoryTestBlockDBModel)
    )
    cursor: AsyncResult = await db_session.execute(query_update)
    await db_session.commit()
    updated_block_laboratory_test: AppointmentLaboratoryTestBlockDBModel = cursor.scalars().first()
    return AppointmentLaboratoryTestBlock.model_validate(updated_block_laboratory_test)
