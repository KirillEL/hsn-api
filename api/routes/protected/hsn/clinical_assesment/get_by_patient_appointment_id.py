from .router import clinical_assesment_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.clinical_assesment import ClinicalAssesment, hsn_clinical_assesment_get_by_patient_appointment_id


@clinical_assesment_router.get(
    "/{patient_appointment_id}",
    response_model=ClinicalAssesment,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_get_clinical_assesment_by_patient_appointment_id(patient_appointment_id: int):
    return await hsn_clinical_assesment_get_by_patient_appointment_id(patient_appointment_id)