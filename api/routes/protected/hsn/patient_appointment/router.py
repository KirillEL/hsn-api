from fastapi import APIRouter


patient_appointment_router = APIRouter(
    prefix="/patient_appointment",
    tags=["Patient Appointment"]
)
