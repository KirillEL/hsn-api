from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MedOrganization(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

    is_deleted: bool
    created_at: datetime
    created_by: str

    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
