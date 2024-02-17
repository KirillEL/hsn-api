from .router import patient_hospitalization_router
from pydantic import BaseModel, Field
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, Response


class CreatePatientHospitalizationRequest(BaseModel):
    pass


@patient_hospitalization_router.post(
    "/",
    response_model="",
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_hospitalization_create(request: Request, req_body: CreatePatientHospitalizationRequest):
    pass
