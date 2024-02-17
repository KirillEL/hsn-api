from .router import patient_hospitalization_router
from pydantic import BaseModel, Field
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, Response


class UpdatePatientHospitalizationRequest(BaseModel):
    pass


@patient_hospitalization_router.put(
    "/{patient_name}",
    response_model="",
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_hospitalization_update_by_patient_name(patient_name: str, request: Request,
                                                             req_body: UpdatePatientHospitalizationRequest):
    pass
