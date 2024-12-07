from domains.shared.db.db_session import SessionContext
from pydantic import BaseModel


class HsnUpdatePatientAppointmentContext(BaseModel):
    user_id: int


@SessionContext()
async def hsn_patient_appointment_update(context: HsnUpdatePatientAppointmentContext):
    pass
