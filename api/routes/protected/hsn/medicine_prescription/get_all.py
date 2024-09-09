from core.hsn.medicine_prescription import MedicinePrescriptionFlat, hsn_medicine_prescription_all
from core.hsn.medicine_prescription.model import MedicinePrescriptionFlatResponse
from .router import medicine_prescription_router
from api.exceptions import ExceptionResponseSchema


@medicine_prescription_router.get(
    "",
    response_model=list[MedicinePrescriptionFlatResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_medicine_prescriptions(limit: int = None, offset: int = None):
    return await hsn_medicine_prescription_all(limit, offset)