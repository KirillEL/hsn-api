from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update

from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from shared.db.db_session import db_session, SessionContext


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
    cd: Optional[bool] = None
    cd_note: Optional[str] = None
    hobl_ba: Optional[bool] = None
    hobl_ba_note: Optional[str] = None
    onmk_tia: Optional[bool] = None
    onmk_tia_note: Optional[str] = None
    hbp: Optional[bool] = None
    hbp_note: Optional[str] = None
    another: Optional[str] = None


@SessionContext()
async def hsn_command_block_diagnose_update(context: HsnCommandBlockDiagnoseUpdateContext):
    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query = (
        select(AppointmentDBModel.block_diagnose_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor = await db_session.execute(query)
    block_diagnose_id = cursor.scalar()
    if block_diagnose_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_update = (
        update(AppointmentDiagnoseBlockDBModel)
        .values(**payload)
        .where(AppointmentDiagnoseBlockDBModel.id == block_diagnose_id)
        .returning(AppointmentDiagnoseBlockDBModel)
    )
    cursor = await db_session.execute(query_update)
    await db_session.commit()
    updated_block_diagnose = cursor.scalars().first()
    return AppointmentDiagnoseBlock.model_validate(updated_block_diagnose)