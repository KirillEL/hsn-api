from fastapi import APIRouter


patient_appointment_router = APIRouter(
    prefix="/patient_appointments",
    tags=["Patient Appointment"]
)
