from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from ..model import Cabinet
from sqlalchemy import insert, select
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.med_organization import MedOrganizationDBModel
from shared.db.commands import db_base_entity_create
from api.exceptions import NotFoundException
from loguru import logger


class HsnCabinetCreateContext(BaseModel):
    user_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=150)
    # add med_id
    med_id: int = Field(gt=0)


@SessionContext()
async def hsn_cabinet_create(context: HsnCabinetCreateContext) -> Cabinet:
    payload = context.model_dump(exclude={'user_id'})

    query_check_med_id = (
        select(MedOrganizationDBModel)
        .where(MedOrganizationDBModel.id == context.med_id)
    )
    cursor_check = await db_session.execute(query_check_med_id)
    med = cursor_check.scalars().first()
    if med is None:
        raise NotFoundException(message="мед учреждение не найдено!")

    query = (
        insert(CabinetDBModel)
        .values(**payload, author_id=context.user_id)
        .returning(CabinetDBModel)
    )
    cursor = await db_session.execute(query)
    new_cabinet = cursor.scalars().first()
    logger.debug(f"new_cabinet:{new_cabinet.__dict__}")
    await db_session.commit()
    return Cabinet.model_validate(new_cabinet)



