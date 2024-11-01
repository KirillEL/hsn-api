from sqlalchemy import Column, Integer, Boolean, String, DateTime, Float, Text
from shared.db.models.BASE import BaseDBModel


class AppointmentLaboratoryTestBlockDBModel(BaseDBModel):
    __tablename__ = 'appointment_block_laboratory_tests'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)

    # гормональный анализ крови
    nt_pro_bnp = Column(Float)
    nt_pro_bnp_date = Column(String(12))
    hbalc = Column(Float)
    hbalc_date = Column(String(12))

    # общий анализ крови
    eritrocit = Column(Float)
    hemoglobin = Column(Float)
    oak_date = Column(String(12))

    # биохим анализ крови
    tg = Column(Float)
    lpvp = Column(Float)
    lpnp = Column(Float)
    general_hc = Column(Float)
    natriy = Column(Float)
    kaliy = Column(Float)
    glukoza = Column(Float)
    mochevaya_kislota = Column(Float)
    skf = Column(Float)
    kreatinin = Column(Float)
    bk_date = Column(String(12))

    # общий анализ мочи
    protein = Column(Float)
    urine_eritrocit = Column(Float)
    urine_leycocit = Column(Float)
    microalbumuria = Column(Float)
    am_date = Column(String(12))

    note = Column(Text)
