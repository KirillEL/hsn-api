from core.hsn.medicine_prescription.queries.fields import hsn_medicine_prescriptions_get_fields, \
    GetMedicinePrescriptionFieldsResponse
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema


@block_purpose_router.get(
    "/fields",
    response_model=list[GetMedicinePrescriptionFieldsResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_medicine_prescriptions_fields():
    return await hsn_medicine_prescriptions_get_fields()