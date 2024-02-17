from .router import patient_hospitalization_router
from api.exceptions import ExceptionResponseSchema
from typing import Optional, List


@patient_hospitalization_router.get(
    "/{patient_name}",
    response_model="",
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_hospitalization_get_by_patient_name(patient_name: str):
    pass