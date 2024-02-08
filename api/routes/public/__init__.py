from fastapi import APIRouter, Depends
from .auth import auth_router
from api.dependencies import AlowAll, PermissionDependency

public_router: APIRouter = APIRouter(prefix="/api/v1", dependencies=[Depends(PermissionDependency([AlowAll]))])
public_router.include_router(auth_router)

__all__ = ["public_router"]

