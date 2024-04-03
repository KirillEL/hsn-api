from .create import *
from .delete import *

from .router import admin_appointment_router

from .complaint import admin_appointment_block_complaint_router

admin_appointment_router.include_router(admin_appointment_router)


__all__ = [
    'admin_appointment_router'
]