from .BASE import BaseDBModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class RoleDBModel(BaseDBModel):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    users = relationship(
        "UserDBModel", secondary="public.user_roles", back_populates="roles"
    )
