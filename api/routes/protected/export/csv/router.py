from fastapi import APIRouter

csv_router = APIRouter(
    prefix="/export/csv",
    tags=["ЭКСПОРТ ДАННЫХ"]
)