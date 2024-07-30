from sqlalchemy import Column, Integer, Boolean, String, DateTime, Float, Text
from shared.db.models.BASE import BaseDBModel


class AppointmentLaboratoryTestBlockDBModel(BaseDBModel):
    __tablename__ = "appointment_block_laboratory_tests"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, nullable=False)

    # гормональный анализ крови
    nt_pro_bnp = Column(Float)
    nt_pro_bnp_date = Column(Text)
    hbalc = Column(Float)
    hbalc_date = Column(Text)

    # общий анализ крови
    eritrocit = Column(Float)
    eritrocit_date = Column(Text)
    hemoglobin = Column(Float)
    hemoglobin_date = Column(Text)

    # биохим анализ крови
    tg = Column(Float)
    tg_date = Column(Text)
    lpvp = Column(Float)
    lpvp_date = Column(Text)
    lpnp = Column(Float)
    lpnp_date = Column(Text)
    general_hc = Column(Float)
    general_hc_date = Column(Text)
    natriy = Column(Float)
    natriy_date = Column(Text)
    kaliy = Column(Float)
    kaliy_date = Column(Text)
    glukoza = Column(Float)
    glukoza_date = Column(Text)
    mochevaya_kislota = Column(Float)
    mochevaya_kislota_date = Column(Text)
    skf = Column(Float)
    skf_date = Column(Text)
    kreatinin = Column(Float)
    kreatinin_date = Column(Text)

    # общий анализ мочи
    protein = Column(Float)
    protein_date = Column(Text)
    urine_eritrocit = Column(Float)
    urine_eritrocit_date = Column(Text)
    urine_leycocit = Column(Float)
    urine_leycocit_date = Column(Text)
    microalbumuria = Column(Float)
    microalbumuria_date = Column(Text)
    note = Column(Text)
