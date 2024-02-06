from fastapi import APIRouter, Depends
from .auth import auth_router

public_router: APIRouter = APIRouter(prefix="/api/v1", dependencies=[])
public_router.include_router(auth_router)

__all__ = ["public_router"]

