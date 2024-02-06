from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class MedicinesCatalog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: float
    name: str

    medicine_group_id: int

    is_deleted: bool

    created_at: datetime
    created_by: str

    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None

