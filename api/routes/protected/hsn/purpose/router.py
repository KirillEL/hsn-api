from fastapi import APIRouter

purpose_router = APIRouter(
    prefix="/purposes",
    tags=["Назначение препаратов"]
)