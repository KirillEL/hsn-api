from shared.db.models.BASE import BaseDBModel
from sqlalchemy import Column, Text, Boolean, DateTime, Integer, Float, String, text


class AppointmentDiagnoseBlockDBModel(BaseDBModel):
    __tablename__ = 'appointment_block_diagnoses'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    diagnose = Column(Text, nullable=False)
    classification_func_classes = Column(String(1), nullable=False)  # 1 2 3 4
    classification_adjacent_release = Column(String(50), nullable=False)  # Низкая / Умеренно-сниженная / сохранная
    classification_nc_stage = Column(String(5), nullable=False)  # I IIa IIб III

    cardiomyopathy = Column(Boolean, nullable=False, server_default=text("false"))
    cardiomyopathy_note = Column(Text)

    ibc_pikc = Column(Boolean, nullable=False, server_default=text("false"))
    ibc_pikc_note = Column(Text)

    ibc_stenocardia_napr = Column(Boolean, nullable=False, server_default=text("false"))
    ibc_stenocardia_napr_note = Column(Text)

    ibc_another = Column(Boolean, nullable=False, server_default=text("false"))
    ibc_another_note = Column(Text)

    fp_tp = Column(Boolean, nullable=False, server_default=text("false"))
    fp_tp_note = Column(Text)

    ad = Column(Boolean, nullable=False, server_default=text("false"))
    ad_note = Column(Text)

    dislipidemia = Column(Boolean, nullable=False, server_default=text("false"))
    dislipidemia_note = Column(Text)

    hobl_ba = Column(Boolean, nullable=False, server_default=text("false"))
    hobl_ba_note = Column(Text)

    onmk_tia = Column(Boolean, nullable=False, server_default=text("false"))
    onmk_tia_note = Column(Text)

    hbp = Column(Boolean, nullable=False, server_default=text("false"))
    hbp_note = Column(Text)

    another = Column(Boolean, nullable=False, server_default=text("false"))
    another_note = Column(Text)
