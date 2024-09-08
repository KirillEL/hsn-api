import csv
from io import StringIO

from api.exceptions import ExceptionResponseSchema, NotFoundException
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
async def export_patients(request: Request):
    current_user_id: int = request.user.id
    result = await hsn_get_own_patients(current_user_id)
    patients = result["data"]
    if len(patients) == 0:
        raise NotFoundException

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["id",
                     "ФИО",
                     "Пол",
                     "Возраст",
                     "Дата рождения",
                     "Дата смерти",
                     "Локация",
                     "Район",
                     "Адрес",
                     "Телефон"
                     ])

    for patient in patients:
        writer.writerow([
            patient.id,
            patient.full_name,
            patient.age,
            patient.birth_date,
            patient.dod,
            patient.location,
            patient.district,
            patient.address,
            patient.phone
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=patients.csv"
        }
    )
