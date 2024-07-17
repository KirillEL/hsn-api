from fastapi import APIRouter

medicine_prescription_router = APIRouter(
    prefix="/medicine_prescriptions",
    tags=["Препараты"]
)