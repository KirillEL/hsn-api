from api.decorators import HandleExceptions
from router import admin_appointment_router
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import SessionContext


@admin_appointment_router.post(
    "/appointments",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
@HandleExceptions()
async def admin_appointment_create():
    pass