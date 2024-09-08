import csv
from io import StringIO

from starlette.responses import StreamingResponse

from api.exceptions import NotFoundException
from core.hsn.patient import hsn_get_own_patients


async def export_patients(user_id: int):
    result = await hsn_get_own_patients(user_id)
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
