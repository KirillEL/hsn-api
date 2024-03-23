from fastapi import APIRouter

appointment_router = APIRouter(
    prefix="/appointments",
    tags=["Приемы"]
)
