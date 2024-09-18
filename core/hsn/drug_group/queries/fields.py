from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.hsn.drug_group.schemas import DrugGroupSchema, DrugGroupFieldsResponse
from shared.db.db_session import SessionContext, db_session
from shared.db.models import DrugDBModel


@SessionContext()
async def hsn_query_drug_group_fields():
    query = (
        select(DrugDBModel)
        .options(
            selectinload(DrugDBModel.drug_group)
        )
        .where(DrugDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    drugs = cursor.scalars().all()
    grouped_prescriptions = {}
    for drug in drugs:
        if drug.drug_group is not None:
            group_name = drug.drug_group.name
            if group_name not in grouped_prescriptions:
                grouped_prescriptions[group_name] = []
            grouped_prescriptions[group_name].append(
                DrugGroupSchema(
                    id=drug.id,
                    displayName=drug.name,
                    description=""
                )
            )

    response = [
        DrugGroupFieldsResponse(
            displayName=group,
            drugs=grouped_prescriptions[group]
        ) for group in grouped_prescriptions
    ]
    return response
