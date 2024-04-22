from .list import *
from .create import *
from .get_by_id import *
from .initialize import *
from .status import *

from .router import appointment_router
from .block_ekg import block_ekg_router
from .block_diagnose import block_diagnose_router
from .block_laboratory_test import block_laboratory_test_router
from .block_clinic_doctor import block_clinic_doctor_router
from .block_clinical_condition import block_clinical_condition_router
from .block_complaint import block_complaint_router
from .block_purpose import block_purpose_router

appointment_router.include_router(block_ekg_router)
appointment_router.include_router(block_diagnose_router)
appointment_router.include_router(block_laboratory_test_router)
appointment_router.include_router(block_clinic_doctor_router)
appointment_router.include_router(block_clinical_condition_router)
appointment_router.include_router(block_complaint_router)
appointment_router.include_router(block_purpose_router)


__all__ = ['appointment_router']