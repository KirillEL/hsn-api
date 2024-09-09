from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from core.hsn.medicine_prescription import MedicinePrescriptionFlat, HsnMedicinePrescriptionCreateContext, \
    hsn_medicine_prescription_create
from core.hsn.medicine_prescription.model import MedicinePrescriptionFlatResponse
from .router import medicine_prescription_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


class MedicineGroupEnum(Enum):
    BAB = "b-АБ"
    GLYPHOZYN = "Глифозины"
    STATIN = "Статины"
    AMKR = "АМКР"
    ARNI = "АРНИ"
    APF = "АПФ"
    SARTAN = "САРТАНЫ"
    ASK = "АСК"
    POAK_AVK = "ПОАК или АВК"
    BMKK = "БМКК"
    NITRAT = "Нитраты"
    DIURETIC = "Диуретики"
    ANTIARITMIC = "Антиаритмики"
    IVABRADIN = "Ивабрадин"
    DIZAGREGANT = "Дизагреганты"
    GLYKOLIS = "Сердечные гликозиды"
    GYPOTENZ = "Гипотензивные"
    ANOTHER = "Другое"


class CreateMedicinePrescriptionRequestBody(BaseModel):
    medicine_group_id: int = Field(gt=0)
    name: str = Field(max_length=500)
    note: Optional[str] = Field(None, max_length=1000)


@medicine_prescription_router.post(
    "",
    response_model=MedicinePrescriptionFlatResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_medicine_prescription(request: Request, body: CreateMedicinePrescriptionRequestBody):
    context = HsnMedicinePrescriptionCreateContext(
        doctor_id=request.user.doctor.id,
        **body.model_dump()
    )
    return await hsn_medicine_prescription_create(context)
