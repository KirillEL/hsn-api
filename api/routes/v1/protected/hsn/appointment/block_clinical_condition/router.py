from fastapi import APIRouter

block_clinical_condition_router = APIRouter(
    prefix="/block/clinical_condition", tags=["Блок клиническое состояние"]
)
