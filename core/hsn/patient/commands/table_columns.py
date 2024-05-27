import json
from sqlalchemy import insert

from api.decorators import HandleExceptions
from core.hsn.patient.model import PatientTableColumns, TableColumns
from shared.db.models.patient_columns import PatientTableColumnsDBModel
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field, ConfigDict


class HsnPatientColumnsCreateContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user_id: int = Field(gt=0)
    table_columns: list[TableColumns]


@SessionContext()
@HandleExceptions()
async def hsn_patient_columns_create(context: HsnPatientColumnsCreateContext):
    serialized_columns = [column.dict() for column in context.table_columns]
    query = (
        insert(PatientTableColumnsDBModel)
        .values(
            user_id=context.user_id,
            table_columns=serialized_columns
        )
        .returning(PatientTableColumnsDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    await db_session.refresh(PatientTableColumnsDBModel)
    new_patient_columns = cursor.scalars().first()
    return PatientTableColumns.model_validate(new_patient_columns)
