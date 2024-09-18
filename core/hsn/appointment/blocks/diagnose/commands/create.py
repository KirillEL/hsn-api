from typing import Optional

from sqlalchemy import insert, update, exc

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import check_appointment_exists
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from pydantic import BaseModel


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

    cd: Optional[bool] = False
    cd_note: Optional[str] = None

    hobl_ba: Optional[bool] = False
    hobl_ba_note: Optional[str] = None

    onmk_tia: Optional[bool] = None
    onmk_tia_note: Optional[str] = None

    hbp: Optional[bool] = False
    hbp_note: Optional[str] = None

    another: Optional[str] = None


@SessionContext()
async def hsn_command_appointment_block_diagnose_create(context: HsnCommandAppointmentBlockDiagnoseCreateContext):
    await check_appointment_exists(context.appointment_id)
    payload = context.model_dump(exclude={'appointment_id'})
    query = (
        insert(AppointmentDiagnoseBlockDBModel)
        .values(**payload)
        .returning(AppointmentDiagnoseBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    new_block_diagnose_id = cursor.scalar()

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(
            block_diagnose_id=new_block_diagnose_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()
    return new_block_diagnose_id
