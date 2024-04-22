from core.hsn.medicine_prescription.queries.fields import hsn_medicine_prescriptions_get_fields, \
    GetMedicinePrescriptionFieldsResponse
from .router import medicine_prescription_router
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel



@medicine_prescription_router.get(
    "/get_fields",
    response_model=list[GetMedicinePrescriptionFieldsResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_medicine_prescriptions_fields():
    return await hsn_medicine_prescriptions_get_fields()
