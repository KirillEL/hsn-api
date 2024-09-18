from fastapi import APIRouter, Depends
from .user import user_router
from .hsn.patient import patient_router
from .hsn.appointment import appointment_router
from api.dependencies import PermissionDependency, IsAuthenticated
from .export.csv import csv_router

protected_router: APIRouter = APIRouter(prefix="/api/v1",
                                        dependencies=[Depends(PermissionDependency([IsAuthenticated]))])

protected_router.include_router(user_router, tags=["Пользователь"])
protected_router.include_router(patient_router)
protected_router.include_router(appointment_router)
protected_router.include_router(csv_router)
__all__ = ["protected_router"]
