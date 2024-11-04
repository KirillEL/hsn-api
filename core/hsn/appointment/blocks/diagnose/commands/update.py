from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update, Select, Result
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.queries import db_query_entity_by_id


class HsnCommandBlockDiagnoseUpdateContext(BaseModel):
    appointment_id: int
    diagnose: Optional[str] = None
    classification_func_classes: Optional[str] = None
    classification_adjacent_release: Optional[str] = None
    classification_nc_stage: Optional[str] = None
    cardiomyopathy: Optional[bool] = None
    cardiomyopathy_note: Optional[str] = None
    ibc_pikc: Optional[bool] = None
    ibc_pikc_note: Optional[str] = None
    ibc_stenocardia_napr: Optional[bool] = None
    ibc_stenocardia_napr_note: Optional[str] = None
    ibc_another: Optional[bool] = None
    ibc_another_note: Optional[str] = None
    fp_tp: Optional[bool] = None
    fp_tp_note: Optional[str] = None
    ad: Optional[bool] = None
    ad_note: Optional[str] = None
    hobl_ba: Optional[bool] = None
    hobl_ba_note: Optional[str] = None
    onmk_tia: Optional[bool] = None
    onmk_tia_note: Optional[str] = None
    hbp: Optional[bool] = None
    hbp_note: Optional[str] = None
    another: Optional[bool] = None
    another_note: Optional[str] = None


@SessionContext()
async def hsn_command_block_diagnose_update(
        doctor_id: int,
        context: HsnCommandBlockDiagnoseUpdateContext
) -> AppointmentDiagnoseBlock:
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(context.appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(context.appointment_id))

    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query: Select = (
        select(AppointmentDBModel.block_diagnose_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    block_diagnose_id: int = cursor.scalar()

    if not block_diagnose_id:
        raise NotFoundException(message="У приема c id:{} нет данного блока".format(context.appointment_id))

    query_update: ReturningUpdate = (
        update(AppointmentDiagnoseBlockDBModel)
        .values(**payload)
        .where(AppointmentDiagnoseBlockDBModel.id == block_diagnose_id)
        .returning(AppointmentDiagnoseBlockDBModel)
    )
    cursor: AsyncResult = await db_session.execute(query_update)
    await db_session.commit()
    updated_block_diagnose: AppointmentDiagnoseBlockDBModel = cursor.scalars().first()
    return AppointmentDiagnoseBlock.model_validate(updated_block_diagnose)
