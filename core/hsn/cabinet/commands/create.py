from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from ..model import Cabinet
from sqlalchemy import insert
from shared.db.models.cabinet import CabinetDBModel


class HsnCabinetCreateContext(BaseModel):
    name: str = Field(..., max_length=150)
    # add med_id
    med_id: int = Field(gt=0)


@SessionContext()
async def hsn_cabinet_create(ctx: HsnCabinetCreateContext) -> Cabinet:
    model = CabinetDBModel(name=ctx.name, med_id=ctx.med_id)
    db_session.add(model)
    await db_session.commit()
    await db_session.refresh(model)
    return Cabinet.model_validate(model)



