from fastapi import APIRouter

auth_verify_router = APIRouter(
    prefix="/verify",
    tags=["Verification"]
)