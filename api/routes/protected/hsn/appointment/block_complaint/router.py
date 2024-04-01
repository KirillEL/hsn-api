from fastapi import APIRouter

block_complaint_router = APIRouter(
    prefix="/block/complaint",
    tags=["Block complaint"]
)