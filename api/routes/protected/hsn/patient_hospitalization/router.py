from fastapi import APIRouter

patient_hospitalization_router = APIRouter(
    prefix="/patient_hospitalization",
    tags=["Patient Hospitalization"]
)
