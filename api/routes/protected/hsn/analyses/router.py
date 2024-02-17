from fastapi import APIRouter

analyses_router = APIRouter(
    prefix="/analyses",
    tags=["Analyses"]
)
