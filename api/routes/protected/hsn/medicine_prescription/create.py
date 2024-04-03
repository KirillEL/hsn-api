from pydantic import BaseModel, Field

from .router import medicine_prescription_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request

class CreateMedicinePrescriptionRequestBody(BaseModel):
    pass

@medicine_prescription_router.post(
    "",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_medicine_prescription(request: Request, body: CreateMedicinePrescriptionRequestBody):
    pass