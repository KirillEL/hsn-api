from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional


class HsnCreatePatientAppontmentContext(BaseModel):
    user_id: int


@SessionContext()
async def hsn_patient_appontment_create(context: HsnCreatePatientAppontmentContext):
    pass
