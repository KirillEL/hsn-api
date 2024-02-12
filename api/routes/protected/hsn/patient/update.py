from .router import patient_router
from .schemas import PatientResponse
from fastapi import Request, Response
from api.exceptions import ExceptionResponseSchema

from pydantic import BaseModel
from typing import Optional


class PatientUpdateRequest(BaseModel):
    name: str
    last_name: str
    patronymic: str
    age: int
    gender: str = Optional[str]
    birth_date: str = Optional[str]


@patient_router.put(
    '/{patient_id}',
    response_model=PatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_update(patient_id: int, req: Request, req_body: PatientUpdateRequest):
    pass