from pydantic import BaseModel, ConfigDict


class AppointmentDrugTherapyBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)
