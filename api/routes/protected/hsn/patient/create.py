from .router import patient_router
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from fastapi import Request, Response


class CreatePatientRequestContext(BaseModel):
    user_id: int = Field(None, gt=0)

    name: str = Field(None, max_length=100)
    last_name: str = Field(None, max_length=100)
    patronymic: Optional[str] = None
    age: int = Field(None, gt=0)
    gender: str = Field(..., max_length=1)

    date_birth: datetime


@patient_router.post(
    "/",
)
async def api_patient_create(request: Request, req_body: CreatePatientRequestContext):
    pass
