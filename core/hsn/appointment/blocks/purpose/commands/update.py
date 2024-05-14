from typing import Optional

from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import select, update, exc
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import db_session, SessionContext


class HsnAppointmentPurposeUpdateContext(BaseModel):
    user_id: int = Field(gt=0)
    appointment_id: int = Field(gt=0)

    medicine_prescription_id: Optional[int] = None
    dosa: Optional[str] = None
    note: Optional[str] = None


@SessionContext()
async def hsn_appointment_purpose_update(context: HsnAppointmentPurposeUpdateContext):
    payload = context.model_dump(exclude={'user_id', 'appointment_id'}, exclude_none=True)

    try:
        query = (
            select(AppointmentPurposeDBModel.id)
            .where(AppointmentPurposeDBModel.is_deleted.is_(False))
            .where(AppointmentPurposeDBModel.appointment_id == context.appointment_id)
        )
        cursor = await db_session.execute(query)
        purpose_id = cursor.scalar()

        if purpose_id is None:
            raise NotFoundException(message="Назначение не найдено!")

        query_update = (
            update(AppointmentPurposeDBModel)
            .values(
                editor_id=context.user_id,
                **payload
            )
            .where(AppointmentPurposeDBModel.is_deleted.is_(False))
            .where(AppointmentPurposeDBModel.id == purpose_id)
        )
        await db_session.execute(query_update)
        await db_session.commit()
        await db_session.refresh(AppointmentPurposeDBModel)

        query_select = (
            select(AppointmentPurposeDBModel)
            .options(selectinload(AppointmentPurposeDBModel.medicine_prescription))
            .where(AppointmentPurposeDBModel.id == purpose_id)
        )
        cursor = await db_session.execute(query_select)
        updated_purpose = cursor.scalar_one()
        return AppointmentPurposeFlat.model_validate(updated_purpose)
    except NotFoundException as ne:
        raise ne
    except exc.SQLAlchemyError as sqle:
        raise UnprocessableEntityException(message=str(sqle))
    except Exception:
        raise InternalServerException


