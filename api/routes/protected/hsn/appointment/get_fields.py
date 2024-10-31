from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.complaint import hsn_query_block_complaint_fields
from core.hsn.appointment.blocks.diagnose import hsn_query_block_diagnose_fields
from core.hsn.appointment.blocks.ekg import hsn_query_block_ekg_fields
from core.hsn.appointment.blocks.laboratory_test import hsn_query_block_laboratory_test_fields
from core.hsn.appointment.model import AppointmentFieldsResponse
from core.hsn.drug_group.queries import hsn_query_drug_group_fields
from .router import appointment_router
from fastapi import Request


@appointment_router.get(
    "/fields",
    response_model=AppointmentFieldsResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    tags=["Прием"]
)
async def get_appointment_fields_route(
        request: Request
):
    diagnose_fields = await hsn_query_block_diagnose_fields()
    complaints = await hsn_query_block_complaint_fields()
    laboratory_test = await hsn_query_block_laboratory_test_fields()
    ekg = await hsn_query_block_ekg_fields()
    purpose = await hsn_query_drug_group_fields()
    response = AppointmentFieldsResponse(
        diagnose=diagnose_fields,
        complaints=complaints,
        laboratory_test=laboratory_test,
        ekg=ekg,
        purpose=purpose
    )
    return response
