from .user import UserDBModel
from .cabinet import CabinetDBModel
from .contragent import ContragentDBModel
from .doctor import DoctorDBModel
from .med_organization import MedOrganizationDBModel

__all__ = [
    'UserDBModel',
    'CabinetDBModel',
    'ContragentDBModel',
    'DoctorDBModel',
    'MedOrganizationDBModel'
]