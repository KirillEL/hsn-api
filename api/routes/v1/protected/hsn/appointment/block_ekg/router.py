from fastapi import APIRouter


block_ekg_router = APIRouter(
    prefix="/block/ekg",
    tags=["Block ekg"]
)