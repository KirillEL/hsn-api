from api.exceptions import (
    ExceptionResponseSchema,
    DoctorNotAssignedException,
)
from domains.core.export.csv.queries.get import export_patients
from .router import csv_router
from fastapi import Request


@csv_router.get(
    "/patients",
    responses={
        "200": {
            "content": {"text/csv": {}},
            "description": "CSV файл с пациентами",
        },
        "400": {"model": ExceptionResponseSchema},
    },
)
async def csv_export_patients(request: Request):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await export_patients(request, doctor_id=request.user.doctor.id)
