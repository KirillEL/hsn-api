from fastapi import APIRouter, Depends
from .user import user_router
from api.dependencies import PermissionDependency, IsAuthenticated

protected_router: APIRouter = APIRouter(prefix="/api/v1",
                                        dependencies=[Depends(PermissionDependency([IsAuthenticated]))])

protected_router.include_router(user_router, tags=["User"])

__all__ = ["protected_router"]
