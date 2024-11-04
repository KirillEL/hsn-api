from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update, Select, Result
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.queries import db_query_entity_by_id


class HsnCommandBlockEkgUpdateContext(BaseModel):
    appointment_id: int
    date_ekg: Optional[str] = None
    sinus_ritm: Optional[bool] = None
    av_blokada: Optional[bool] = None
    hypertrofia_lg: Optional[bool] = None
    ritm_eks: Optional[bool] = None
    av_uzlovaya_tahikardia: Optional[bool] = None
    superventrikulyrnaya_tahikardia: Optional[bool] = None
    zheludochnaya_tahikardia: Optional[bool] = None
    fabrilycia_predcerdiy: Optional[bool] = None
    trepetanie_predcerdiy: Optional[bool] = None
    another_changes: Optional[str] = None
    date_echo_ekg: Optional[str] = None
    fv: Optional[int] = None
    sdla: Optional[int] = None
    lp: Optional[int] = None
    lp2: Optional[int] = None
    pp: Optional[int] = None
    pp2: Optional[int] = None
    kdr_lg: Optional[int] = None
    ksr_lg: Optional[int] = None
    kdo_lg: Optional[int] = None
    kso_lg: Optional[int] = None
    mgp: Optional[int] = None
    zslg: Optional[int] = None
    local_hypokines: Optional[bool] = None
    distol_disfunction: Optional[bool] = None
    anevrizma: Optional[bool] = None
    note: Optional[str] = None


@SessionContext()
async def hsn_command_block_ekg_update(
        doctor_id: int,
        context: HsnCommandBlockEkgUpdateContext
) -> AppointmentEkgBlock:
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(context.appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(context.appointment_id))

    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query: Select = (
        select(AppointmentDBModel.block_ekg_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_ekg_id: int = cursor.scalar()

    if not block_ekg_id:
        raise NotFoundException(message="У приема c id:{} нет данного блока".format(context.appointment_id))

    query_update: ReturningUpdate = (
        update(AppointmentEkgBlockDBModel)
        .values(**payload)
        .where(AppointmentEkgBlockDBModel.id == block_ekg_id)
        .returning(AppointmentEkgBlockDBModel)
    )
    cursor: Result = await db_session.execute(query_update)
    await db_session.commit()
    updated_block_ekg: AppointmentEkgBlockDBModel = cursor.scalars().first()
    return AppointmentEkgBlock.model_validate(updated_block_ekg)
