from core.hsn.patient import hsn_patient_columns
from core.hsn.patient.schemas import PatientTableResponse
from .router import patient_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request




@patient_router.get(
    "/table/columns",
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Получить настройки таблицы для пациентов"
)
async def get_patient_table_columns(request: Request):
    return await hsn_patient_columns(user_id=request.user.id)