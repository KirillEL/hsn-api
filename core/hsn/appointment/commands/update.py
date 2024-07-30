from shared.db import Transaction
from shared.db.db_session import session
from pydantic import BaseModel

from shared.db.transaction import Propagation


class HsnUpdatePatientAppointmentContext(BaseModel):
    user_id: int


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_patient_appointment_update(context: HsnUpdatePatientAppointmentContext):
    pass
