import json
from sqlalchemy import insert, update, select

from api.decorators import HandleExceptions
from core.hsn.patient.model import PatientTableColumns, TableColumns
from core.hsn.patient.queries.get_table_columns import default_payload
from shared.db.models.patient_columns import PatientTableColumnsDBModel
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field, ConfigDict


class HsnPatientColumnsCreateContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user_id: int = Field(gt=0)
    table_columns: list[TableColumns]


async def create_default_columns_settings(user_id:int):
    query = (
        select(PatientTableColumnsDBModel)
        .where(PatientTableColumnsDBModel.user_id == user_id)
    )
    cursor = await db_session.execute(query)
    exists = cursor.scalars().first()
    if not exists:
        default_columns = [{"dataIndex": column["dataIndex"], "hidden": False} for column in default_payload]
        query = (
            insert(PatientTableColumnsDBModel)
            .values(
                user_id=user_id,
                table_columns=default_columns
            )
            .returning(PatientTableColumnsDBModel.id)
        )
        cursor = await db_session.execute(query)
        await db_session.commit()
        return cursor.scalar_one()
    return exists.id

@SessionContext()
@HandleExceptions()
async def hsn_patient_columns_create(context: HsnPatientColumnsCreateContext):
    created_default_columns_id = await create_default_columns_settings(context.user_id)
    serialized_columns = [column.dict() for column in context.table_columns]
    query = (
        update(PatientTableColumnsDBModel)
        .values(
            table_columns=serialized_columns
        )
        .where(PatientTableColumnsDBModel.id == created_default_columns_id)
        .returning(PatientTableColumnsDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_patient_columns = cursor.scalars().first()
    return PatientTableColumns.model_validate(new_patient_columns)
