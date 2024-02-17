from .router import patient_hospitalization_router
from pydantic import BaseModel, Field
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, Response


@patient_hospitalization_router.delete(
    "/{patient_hospitalization_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_hospitalization_delete(patient_hospitalization_id: int, request: Request):
    pass
