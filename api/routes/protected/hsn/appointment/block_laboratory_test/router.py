from fastapi import APIRouter

block_laboratory_test_router = APIRouter(
    prefix="/block/laboratory_test",
    tags=["Block laboratory test"]
)