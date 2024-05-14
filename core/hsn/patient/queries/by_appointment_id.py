from pydantic import ValidationError
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, InternalServerException, ValidationException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose.commands.create import check_appointment_exists
from core.hsn.patient.commands.create import convert_to_patient_response
from core.hsn.patient.model import PatientResponse, PatientResponseWithoutFullName
from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel


@SessionContext()
async def hsn_get_patient_by_appointment_id(appointment_id: int):
    try:
        await check_appointment_exists(appointment_id)
        query = (
            select(AppointmentDBModel)
            .options(selectinload(AppointmentDBModel.patient), selectinload(AppointmentDBModel.patient).selectinload(PatientDBModel.contragent))
            .where(AppointmentDBModel.id == appointment_id)
        )
        cursor = await db_session.execute(query)
        appointment = cursor.scalars().first()
        patient_response = await convert_to_patient_response(appointment.patient, type="without")

        return PatientResponseWithoutFullName.model_validate(patient_response)
    except NotFoundException as ne:
        raise ne
    except ValidationError as ve:
        raise ValidationException(message=str(ve))
    except exc.SQLAlchemyError as sqle:
        raise UnprocessableEntityException(message=str(sqle))
    except Exception:
        raise InternalServerException
