from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Cabinet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    med_id: int

    is_deleted: bool
    created_at: datetime
    created_by: str

    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
