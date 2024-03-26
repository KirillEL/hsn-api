from sqlalchemy import Column, Integer, Boolean, String, DateTime, Float, Text
from shared.db.models.BASE import BaseDBModel


class AppointmentLaboratoryTestBlockDBModel(BaseDBModel):
    __tablename__ = 'appointment_block_laboratory_tests'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)

    # гормональный анализ крови
    nt_pro_bnp = Column(Float)
    nt_pro_bnp_date = Column(DateTime(timezone=False))
    hbalc = Column(Float)
    hbalc_date = Column(DateTime(timezone=False))

    # общий анализ крови
    eritrocit = Column(Float)
    eritrocit_date = Column(DateTime(timezone=False))
    hemoglobin = Column(Float)
    hemoglobin_date = Column(DateTime(timezone=False))

    # биохим анализ крови
    tg = Column(Float)
    tg_date = Column(DateTime(timezone=False))
    lpvp = Column(Float)
    lpvp_date = Column(DateTime(timezone=False))
    lpnp = Column(Float)
    lpnp_date = Column(DateTime(timezone=False))
    general_hc = Column(Float)
    general_hc_date = Column(DateTime(timezone=False))
    natriy = Column(Float)
    natriy_date = Column(DateTime(timezone=False))
    kaliy = Column(Float)
    kaliy_date = Column(DateTime(timezone=False))
    glukoza = Column(Float)
    glukoza_date = Column(DateTime(timezone=False))
    mochevaya_kislota = Column(Float)
    mochevaya_kislota_date = Column(DateTime(timezone=False))
    skf = Column(Float)
    skf_date = Column(DateTime(timezone=False))
    kreatinin = Column(Float)
    kreatinin_date = Column(DateTime(timezone=False))

    # общий анализ мочи
    protein = Column(Float)
    protein_date = Column(DateTime(timezone=False))
    urine_eritrocit = Column(Float)
    urine_eritrocit_date = Column(DateTime(timezone=False))
    urine_leycocit = Column(Float)
    urine_leycocit_date = Column(DateTime(timezone=False))
    microalbumuria = Column(Float)
    microalbumuria_date = Column(DateTime(timezone=False))
    note = Column(Text)
