from fastapi import APIRouter, Depends
from api.dependencies.permission import IsAuthenticatedAdministrator
from api.dependencies import PermissionDependency

from .users import admin_users_router
from .patients import admin_patient_router
from .roles import admin_role_router
from .cabinets import admin_cabinet_router
from .med_organization import admin_med_org_router
from .patient_appointments import admin_patient_appointment_router

admin_router: APIRouter = APIRouter(prefix="/api/v1/admin",
                                    dependencies=[Depends(PermissionDependency([IsAuthenticatedAdministrator]))],
                                    tags=["ADMIN"])

admin_router.include_router(admin_users_router)
admin_router.include_router(admin_patient_router)
admin_router.include_router(admin_role_router)
admin_router.include_router(admin_cabinet_router)
admin_router.include_router(admin_med_org_router)
admin_router.include_router(admin_patient_appointment_router)