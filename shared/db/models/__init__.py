from .user import UserDBModel
from .cabinet import CabinetDBModel
from .contragent import ContragentDBModel
from .doctor import DoctorDBModel
from .med_organization import MedOrganizationDBModel
from .patient import PatientDBModel
from .diagnoses_catalog import DiagnosesCatalogDBModel
from .patient_hospitalization import PatientHospitalizationsDBModel
from .supplied_diagnoses import SuppliedDiagnosesDBModel
from .patient_appointment import PatientAppointmentsDBModel
from .medicines_prescription import MedicinesPrescriptionDBModel
from .medicines_group import MedicinesGroupDBModel
from .analyses import AnalysesDBModel
from .researchs import ResearchDBModel
from .clinical_assesment import ClinicalAssesmentDBModel


__all__ = [
    'UserDBModel',
    'CabinetDBModel',
    'ContragentDBModel',
    'DoctorDBModel',
    'MedOrganizationDBModel',
    'PatientDBModel',
    'PatientHospitalizationsDBModel',
    'MedicinesPrescriptionDBModel',
    'MedicinesGroupDBModel',
    'SuppliedDiagnosesDBModel',
    'DiagnosesCatalogDBModel',
    'PatientAppointmentsDBModel',
    'AnalysesDBModel',
    'ResearchDBModel',
    'ClinicalAssesmentDBModel'
]