from domains.core.hsn.patient import hsn_patient_columns_create, HsnPatientColumnsCreateContext
from domains.core.hsn.patient.model import PatientTableColumns, TableColumns
from .router import patient_router
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel
from fastapi import Request


class CreatePatientTableColumnsRequest(BaseModel):
    table_columns: list[TableColumns]


@patient_router.patch(
    "/table/columns",
    response_model=PatientTableColumns,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Создать настройки для таблицы пациентов",
)
async def create_patient_table_columns_route(
    request: Request, payload: CreatePatientTableColumnsRequest
):
    context = HsnPatientColumnsCreateContext(
        user_id=request.user.id, table_columns=payload.table_columns
    )
    return await hsn_patient_columns_create(context)
