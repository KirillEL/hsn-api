from fastapi import Request, Response
from .router import patient_router

from api.exceptions import ExceptionResponseSchema


@patient_router.delete(
    '/{patient_id}',
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_delete(patient_id: int, request: Request) -> bool:
    #
    return True