from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

from core.hsn import Base


class MedicinesCatalog(Base):
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


class MedicineCatalogFlat(Base):
    id: int
    code: float
    name: str
    medicine_group_id: int
