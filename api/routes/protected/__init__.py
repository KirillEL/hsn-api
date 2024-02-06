from fastapi import APIRouter
from .user import user_router
from .hsn import patient_router

protected_router: APIRouter = APIRouter(prefix="/api/v1", dependencies=[])
protected_router.include_router(user_router, tags=["User"])
protected_router.include_router(patient_router, tags=["Patient"])

__all__ = ["protected_router"]