import csv
from io import StringIO

from api.exceptions import ExceptionResponseSchema, NotFoundException, DoctorNotAssignedException
from core.export.csv.queries.get import export_patients
from core.hsn.patient import hsn_get_own_patients
from .router import csv_router
from starlette.responses import StreamingResponse
from fastapi import Request


@csv_router.get(
    "/patients",
    responses={
        '200': {
            "content": {"text/csv": {}},
            "description": "CSV файл с пациентами",
        },
        '400': {"model": ExceptionResponseSchema}
    },
)
async def csv_export_patients(request: Request):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await export_patients(user_id=request.user.id)
