from fastapi import Request, Response
from .router import patient_router

from api.exceptions import ExceptionResponseSchema


@patient_router.delete(
    '/{patient_id}',
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def delete_patient(patient_id: int, req: Request) -> bool:
    #
    return True