from sqlalchemy import select

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.patient.model import PatientTableColumns, PatientTableResponse
from shared.db.models.patient_columns import PatientTableColumnsDBModel
from shared.db.db_session import db_session, SessionContext



@SessionContext()
@HandleExceptions()
async def hsn_patient_columns(user_id: int):
    query = (
        select(PatientTableColumnsDBModel)
        .where(PatientTableColumnsDBModel.user_id == user_id)
    )
    cursor = await db_session.execute(query)
    patient_table_columns = cursor.scalars().first()
    if not patient_table_columns:
        raise NotFoundException(message="Настройки не найдены")

    return PatientTableResponse.model_validate(patient_table_columns)