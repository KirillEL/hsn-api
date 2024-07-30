from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from core.hsn import Base
from core.user import UserAuthor


class MedOrganization(Base):
    id: int
    name: str
    number: int
    address: str

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class MedOrganizationFlat(Base):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int
    name: str
