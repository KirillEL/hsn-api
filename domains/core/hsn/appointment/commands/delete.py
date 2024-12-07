from domains.shared.db.db_session import SessionContext
from pydantic import BaseModel


class HsnDeletePatientAppointmentContext(BaseModel):
    id: int
    patient_appointment_id: int


@SessionContext()
async def hsn_patient_appointment_delete(context: HsnDeletePatientAppointmentContext):
    pass
