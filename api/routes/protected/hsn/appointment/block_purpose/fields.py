from domains.core.hsn.drug_group.queries import hsn_query_drug_group_fields
from domains.core.hsn.drug_group.schemas import DrugGroupFieldsResponse
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@block_purpose_router.get(
    "/fields",
    response_model=list[DrugGroupFieldsResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_medicine_prescriptions_fields(request: Request):
    return await hsn_query_drug_group_fields()
