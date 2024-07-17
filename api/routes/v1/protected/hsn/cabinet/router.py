from fastapi import APIRouter


cabinet_router = APIRouter(
    prefix="/cabinets",
    tags=["Кабинеты"]
)