from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.export.csv.queries.get_all import export_all_appointments
from .router import csv_router
from fastapi import Request


@csv_router.get(
    "/all",
    responses={
        "200": {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "CSV файл с пациентами",
        },
        "400": {"model": ExceptionResponseSchema},
    },
)
async def get_all_appointments(request: Request):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await export_all_appointments(request, request.user.doctor.id)
