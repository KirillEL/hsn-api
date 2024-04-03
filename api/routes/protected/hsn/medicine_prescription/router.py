from fastapi import APIRouter

medicine_prescription_router = APIRouter(
    "/medicine_prescriptions",
    tags=["Назначение препаратов"]
)