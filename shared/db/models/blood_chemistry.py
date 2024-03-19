from .BASE import BaseDBModel
from sqlalchemy import Column, Integer, String, Text, text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship


class BloodChemistryDBModel(BaseDBModel):
    __tablename__ = 'blood_chemistries'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)

    lpnp = Column(Float)
    lpnp_date = Column(DateTime(timezone=False))
    general_hs = Column(Float)
    general_hs_date = Column(DateTime(timezone=False))
    natriy = Column(Float)
    natriy_date = Column(DateTime(timezone=False))
    kaliy = Column(Float)
    kaliy_date = Column(DateTime(timezone=False))
    ferritin = Column(Float)
    ferritin_date = Column(DateTime(timezone=False))
    transferrin = Column(Float)
    transferrin_date = Column(DateTime(timezone=False))
    glukoza = Column(Float)
    glukoza_date = Column(DateTime(timezone=False))
    mochevaya_kta = Column(Float)
    mochevaya_kta_date = Column(DateTime(timezone=False))
    skf = Column(Float)
    skf_date = Column(DateTime(timezone=False))
    kreatin = Column(Float)
    kreatin_date = Column(DateTime(timezone=False))


