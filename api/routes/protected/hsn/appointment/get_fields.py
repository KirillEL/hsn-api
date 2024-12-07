from api.exceptions import ExceptionResponseSchema
from domains.core.hsn.appointment.blocks.clinical_condition import (
    hsn_query_block_clinical_condition_fields,
)
from domains.core.hsn.appointment.blocks.complaint import (
    hsn_query_block_complaint_fields,
)
from domains.core.hsn.appointment.blocks.diagnose import hsn_query_block_diagnose_fields
from domains.core.hsn.appointment.blocks.ekg import hsn_query_block_ekg_fields
from domains.core.hsn.appointment.blocks.laboratory_test import (
    hsn_query_block_laboratory_test_fields,
)
from domains.core.hsn.appointment.model import AppointmentFieldsResponse
from domains.core.hsn.drug_group.queries import hsn_query_drug_group_fields
from .router import appointment_router
from fastapi import Request


@appointment_router.get(
    "/fields",
    response_model=AppointmentFieldsResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    tags=["Прием"],
)
async def get_appointment_fields_route(request: Request):
    diagnose_fields = await hsn_query_block_diagnose_fields()
    complaints = await hsn_query_block_complaint_fields()
    laboratory_test = await hsn_query_block_laboratory_test_fields()
    ekg = await hsn_query_block_ekg_fields()
    purpose = await hsn_query_drug_group_fields()
    clinical_condition = await hsn_query_block_clinical_condition_fields()
    response = AppointmentFieldsResponse(
        diagnose=diagnose_fields,
        complaints=complaints,
        laboratory_test=laboratory_test,
        ekg=ekg,
        purpose=purpose,
        clinical_condition=clinical_condition,
    )
    return response
