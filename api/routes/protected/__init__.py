from fastapi import APIRouter, Depends
from .user import user_router
from .hsn.patient import patient_router
from api.dependencies import PermissionDependency, IsAuthenticated

protected_router: APIRouter = APIRouter(prefix="/api/v1",
                                        dependencies=[Depends(PermissionDependency([IsAuthenticated]))])

protected_router.include_router(user_router, tags=["User"])
protected_router.include_router(patient_router)

__all__ = ["protected_router"]
