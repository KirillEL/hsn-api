from .router import patient_router
from pydantic import BaseModel, Field
from typing import Optional


class CreatePatientRequestContext(BaseModel):
    name: str
    last_name: str
    patronymic: Optional[str] = None
    age: int
    gender: str = Field(..., max_length=1)

    date_birth: str


@patient_router.post(
    "/",
)
async def create_patient(payload: CreatePatientRequestContext):
    pass