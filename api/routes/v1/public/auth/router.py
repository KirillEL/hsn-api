from fastapi import APIRouter
from .login import auth_login_router
from .register import auth_register_router
from .verify import auth_verify_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(auth_login_router)
auth_router.include_router(auth_register_router)
auth_router.include_router(auth_verify_router)
