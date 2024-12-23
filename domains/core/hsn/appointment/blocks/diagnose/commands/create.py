from typing import Optional

from sqlalchemy import insert, update, Update, Result
from sqlalchemy.sql.dml import ReturningInsert

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from domains.shared.db.models.appointment.blocks.block_diagnose import (
    AppointmentDiagnoseBlockDBModel,
)
from pydantic import BaseModel

from domains.shared.db.queries import db_query_entity_by_id


class HsnCommandAppointmentBlockDiagnoseCreateContext(BaseModel):
    appointment_id: int
    diagnose: str
    classification_func_classes: str
    classification_adjacent_release: str
    classification_nc_stage: str

    cardiomyopathy: Optional[bool] = False
    cardiomyopathy_note: Optional[str] = None

    ibc_pikc: Optional[bool] = False
    ibc_pikc_note: Optional[str] = None

    ibc_stenocardia_napr: Optional[bool] = False
    ibc_stenocardia_napr_note: Optional[str] = None

    ibc_another: Optional[bool] = False
    ibc_another_note: Optional[str] = None

    fp_tp: Optional[bool] = False
    fp_tp_note: Optional[str] = None

    ad: Optional[bool] = False
    ad_note: Optional[str] = None

    hobl_ba: Optional[bool] = False
    hobl_ba_note: Optional[str] = None

    onmk_tia: Optional[bool] = None
    onmk_tia_note: Optional[str] = None

    hbp: Optional[bool] = False
    hbp_note: Optional[str] = None

    another: Optional[bool] = False
    another_note: Optional[str] = None


@SessionContext()
async def hsn_command_appointment_block_diagnose_create(
    doctor_id: int, context: HsnCommandAppointmentBlockDiagnoseCreateContext
) -> int:
    appointment: AppointmentDBModel = await db_query_entity_by_id(
        AppointmentDBModel, context.appointment_id
    )

    if not appointment:
        raise NotFoundException(
            message="Прием c id:{} не найден".format(context.appointment_id)
        )

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            "У вас нет прав для доступа к приему с id:{}".format(context.appointment_id)
        )

    payload = context.model_dump(exclude={"appointment_id"})

    query: ReturningInsert = (
        insert(AppointmentDiagnoseBlockDBModel)
        .values(**payload)
        .returning(AppointmentDiagnoseBlockDBModel.id)
    )
    cursor: Result = await db_session.execute(query)
    new_block_diagnose_id: int = cursor.scalar()

    query_update_appointment: Update = (
        update(AppointmentDBModel)
        .values(block_diagnose_id=new_block_diagnose_id)
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()
    return new_block_diagnose_id
