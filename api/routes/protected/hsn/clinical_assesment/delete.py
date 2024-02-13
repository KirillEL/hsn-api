from .router import clinical_assesment_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.clinical_assesment import hsn_clinical_assesment_delete


@clinical_assesment_router.delete(
    "/{clinical_assesment_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_clinical_assesment_delete(clinical_assesment_id: int):
    await hsn_clinical_assesment_delete(clinical_assesment_id)
    return True
