from typing import Optional

from sqlalchemy import update
from .router import admin_doctor_router
from shared.db.models.doctor import DoctorDBModel
from core.hsn.doctor import Doctor
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from fastapi import Request

@admin_doctor_router.delete(
    "/doctors/{doctor_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_doctor_delete(doctor_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }
    query = (
        update(DoctorDBModel)
        .values(**payload)
        .where(DoctorDBModel.id == doctor_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True