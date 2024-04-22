from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select


from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from shared.db.db_session import db_session, SessionContext

class MedicinePrescriptionSchema(BaseModel):
    id: int
    displayName: str
    description: str


class GetMedicinePrescriptionFieldsResponse(BaseModel):
    displayName: str
    medicine_prescriptions: list[MedicinePrescriptionSchema]

@SessionContext()
async def hsn_medicine_prescriptions_get_fields():
    try:
        result = await db_session.execute(select(MedicinesPrescriptionDBModel))
        prescriptions = result.scalars().all()
        grouped_prescriptions = {}
        for prescription in prescriptions:
            if prescription.medicine_group not in grouped_prescriptions:
                grouped_prescriptions[prescription.medicine_group] = []
            grouped_prescriptions[prescription.medicine_group].append(
                MedicinePrescriptionSchema(
                    id=prescription.id,
                    displayName=prescription.name,
                    description=prescription.note or ""
                )
            )

        # Create the response list
        response = [
            GetMedicinePrescriptionFieldsResponse(
                displayName=group,
                medicine_prescriptions=grouped_prescriptions[group]
            )
            for group in grouped_prescriptions
        ]
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
