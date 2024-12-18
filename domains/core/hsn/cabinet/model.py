from datetime import datetime
from typing import Optional

from domains.core.hsn.med_organization import MedOrganizationFlat
from domains.core.user.model import UserAuthor
from pydantic import BaseModel, ConfigDict


class Cabinet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    med_id: Optional[int] = None

    is_deleted: bool
    created_at: datetime

    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class CabinetFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    med_id: int
    is_deleted: bool


class CabinetWithMedOrganizationFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    med_id: int
    med_org: MedOrganizationFlat
    is_deleted: bool
