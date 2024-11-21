from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from ..model import Cabinet
from sqlalchemy import insert, select
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.med_organization import MedOrganizationDBModel
from shared.db.commands import db_base_entity_create
from api.exceptions import NotFoundException, BadRequestException
from loguru import logger


class HsnCabinetCreateContext(BaseModel):
    user_id: int = Field(..., gt=0)
    number: str = Field(..., max_length=200)
    med_id: int = Field(gt=0)


async def check_med_organization_exists(med_id: int):
    query = select(MedOrganizationDBModel).where(MedOrganizationDBModel.id == med_id)
    result = await db_session.execute(query)
    med_organization = result.scalars().first()
    if med_organization is None:
        raise NotFoundException(message="Мед учреждение не найдено!")


@SessionContext()
async def hsn_cabinet_create(context: HsnCabinetCreateContext) -> Cabinet:
    await check_med_organization_exists(context.med_id)
    payload = context.model_dump(exclude={"user_id"})

    query = (
        insert(CabinetDBModel)
        .values(**payload, author_id=context.user_id)
        .returning(CabinetDBModel)
    )
    cursor = await db_session.execute(query)
    new_cabinet = cursor.scalars().first()

    try:
        await db_session.commit()
        logger.debug(f"New Cabinet created: {new_cabinet.id}")
        return Cabinet.model_validate(new_cabinet)
    except Exception as e:
        logger.error(f"Error creating cabinet: {e}")
        await db_session.rollback()
        raise BadRequestException(message=str(e))
