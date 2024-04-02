from fastapi import APIRouter, Depends
from api.dependencies.permission import IsAuthenticatedAdministrator
from api.dependencies import PermissionDependency

from .users import admin_users_router
from .patients import admin_patient_router
from .roles import admin_role_router
from .cabinets import admin_cabinet_router
from .med_organization import admin_med_org_router
from .patient_hospitalizations import admin_patient_hospitalization_router
from .analises import admin_analises_router
from .researchs import admin_researchs_router
from .diagnose_catalog import admin_diagnose_catalog_router
from .doctors import admin_doctor_router
from .supplied_diagnoses import admin_supplied_diagnose_router
from .medicine_prescription import admin_medicine_prescription_router
from .clinical_assesment import admin_clinical_assesment_router

admin_router: APIRouter = APIRouter(prefix="/api/v1/admin",
                                    dependencies=[Depends(PermissionDependency([IsAuthenticatedAdministrator]))],
                                    tags=["ADMIN"])


admin_router.include_router(admin_users_router)
admin_router.include_router(admin_patient_router)
admin_router.include_router(admin_role_router)
admin_router.include_router(admin_cabinet_router)
admin_router.include_router(admin_med_org_router)
admin_router.include_router(admin_patient_hospitalization_router)
admin_router.include_router(admin_analises_router)
admin_router.include_router(admin_researchs_router)
admin_router.include_router(admin_diagnose_catalog_router)
admin_router.include_router(admin_doctor_router)
admin_router.include_router(admin_supplied_diagnose_router)
admin_router.include_router(admin_medicine_prescription_router)
admin_router.include_router(admin_clinical_assesment_router)