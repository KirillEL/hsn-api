from fastapi import APIRouter

block_drug_therapy_router = APIRouter(
    prefix="/block/drug_therapy",
    tags=["Block drug therapy"]
)
