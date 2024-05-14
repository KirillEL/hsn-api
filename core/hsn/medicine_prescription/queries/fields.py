from fastapi import HTTPException
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select, exc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from api.exceptions import InternalServerException
from api.exceptions.base import UnprocessableEntityException
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
        result = await db_session.execute(
            select(MedicinesPrescriptionDBModel)
            .options(selectinload(MedicinesPrescriptionDBModel.medicine_group))
            .where(MedicinesPrescriptionDBModel.is_deleted.is_(False))
        )
        prescriptions = result.scalars().all()
        grouped_prescriptions = {}
        for prescription in prescriptions:
            if prescription.medicine_group is not None:
                group_name = prescription.medicine_group.name
                if group_name not in grouped_prescriptions:
                    grouped_prescriptions[group_name] = []
                grouped_prescriptions[group_name].append(
                    MedicinePrescriptionSchema(
                        id=prescription.id,
                        displayName=prescription.name,
                        description=prescription.note or ""
                    )
                )

        response = [
            GetMedicinePrescriptionFieldsResponse(
                displayName=group,
                medicine_prescriptions=grouped_prescriptions[group]
            ) for group in grouped_prescriptions
        ]
        return response
    except exc.SQLAlchemyError as sqle:
        raise UnprocessableEntityException(message=str(sqle))
    except Exception as e:
        raise InternalServerException


