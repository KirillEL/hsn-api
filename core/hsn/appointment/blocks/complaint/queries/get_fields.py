from loguru import logger
from sqlalchemy import inspect

from core.hsn.appointment.blocks.complaint.model import AppointmentBlockBooleanFieldsResponse
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel


@SessionContext()
async def hsn_query_block_complaint_fields():
    inspector = inspect(AppointmentComplaintBlockDBModel)
    field_responses = []

    display_names = {
        "has_fatigue": "Утомляемость",
        "has_dyspnea": "Одышка",
        "increased_ad": "Повышение АД",
        "rapid_heartbeat": "Учащенное сердцебиение",
        "has_swelling_legs": "Отеки",
        "has_weakness": "Слабость",
        "has_orthopnea": "Ортопноэ",
        "note": ""
    }

    for column in inspector.columns.values():
        field_name = column.name
        if field_name != "id" and field_name != "note":
            field_response = AppointmentBlockBooleanFieldsResponse(
                name=field_name,
                displayName=display_names.get(field_name, ""),
                secondName=""
            )
            field_responses.append(field_response)

    return field_responses
