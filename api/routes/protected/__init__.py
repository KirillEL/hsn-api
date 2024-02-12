from fastapi import APIRouter, Depends
from .user import user_router
from .hsn import patient_router, cabinet_router
from api.dependencies import PermissionDependency, IsAuthenticated
from .hsn.med_organization import med_org_router

protected_router: APIRouter = APIRouter(prefix="/api/v1",
                                        dependencies=[Depends(PermissionDependency([IsAuthenticated]))])

protected_router.include_router(user_router, tags=["User"])
protected_router.include_router(patient_router, tags=["Patient"])
protected_router.include_router(cabinet_router, tags=["Cabinet"])
protected_router.include_router(med_org_router)

__all__ = ["protected_router"]
