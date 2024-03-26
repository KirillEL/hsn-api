from typing import Optional

from sqlalchemy import insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from pydantic import BaseModel

class HsnAppointmentBlockDiagnoseCreateContext(BaseModel):
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
async def hsn_appointment_block_diagnose_create(context: HsnAppointmentBlockDiagnoseCreateContext):
    query = (
        insert(AppointmentDiagnoseBlockDBModel)
        .values(**context.model_dump())
        .returning(AppointmentDiagnoseBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_block_diagnose_id = cursor.scalar()
    return new_block_diagnose_id