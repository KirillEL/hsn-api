from fastapi import APIRouter

from api.routes.v1.public import public_router
from api.routes.v1.protected import protected_router

main_router: APIRouter = APIRouter()
main_router.include_router(public_router)
main_router.include_router(protected_router)

__all__ = ["main_router"]
