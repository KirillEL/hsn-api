from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class UserRoleDBModel(BaseDBModel):
    __tablename__ = 'user_roles'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('public.users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('public.roles.id'), primary_key=True)
