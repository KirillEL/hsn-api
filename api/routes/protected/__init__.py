from fastapi import APIRouter, Depends
from .user import user_router
from .hsn.patient import patient_router
from .hsn.appointment import appointment_router
from .hsn.purpose import purpose_router
from api.dependencies import PermissionDependency, IsAuthenticated
from .hsn.medicine_prescription import medicine_prescription_router

protected_router: APIRouter = APIRouter(prefix="/api/v1",
                                        dependencies=[Depends(PermissionDependency([IsAuthenticated]))])

protected_router.include_router(user_router, tags=["Пользователь"])
protected_router.include_router(patient_router)
protected_router.include_router(appointment_router)
protected_router.include_router(purpose_router)
protected_router.include_router(medicine_prescription_router)
__all__ = ["protected_router"]
