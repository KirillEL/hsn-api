from sqlalchemy import Column, Integer, String, DateTime, Boolean, text, Text, Float
from shared.db.models.BASE import BaseDBModel


class AppointmentEkgBlockDBModel(BaseDBModel):
    __tablename__ = 'appointment_block_ekgs'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    date_ekg = Column(Text, nullable=False)
    sinus_ritm = Column(Boolean, nullable=False, server_default=text("false"))
    av_blokada = Column(Boolean, nullable=False, server_default=text("false"))
    hypertrofia_lg = Column(Boolean, nullable=False, server_default=text("false"))
    ritm_eks = Column(Boolean, nullable=False, server_default=text("false"))
    av_uzlovaya_tahikardia = Column(Boolean, nullable=False, server_default=text("false"))
    superventrikulyrnaya_tahikardia = Column(Boolean, nullable=False, server_default=text("false"))
    zheludochnaya_tahikardia = Column(Boolean, nullable=False, server_default=text("false"))
    fabrilycia_predcerdiy = Column(Boolean, nullable=False, server_default=text("false"))
    trepetanie_predcerdiy = Column(Boolean, nullable=False, server_default=text("false"))
    another_changes = Column(Text)

    date_echo_ekg = Column(Text, nullable=False)
    fv = Column(Float, nullable=False)
    sdla = Column(Float)
    lp = Column(Float)
    pp = Column(Float)
    kdr_lg = Column(Float)
    ksr_lg = Column(Float)
    kdo_lg = Column(Float)
    mgp = Column(Float)
    zslg = Column(Float)
    local_hypokines = Column(Boolean, nullable=False, server_default=text("false"))
    difusal_hypokines = Column(Boolean, nullable=False, server_default=text("false"))
    distol_disfunction = Column(Boolean, nullable=False, server_default=text("false"))
    valvular_lesions = Column(Boolean, nullable=False, server_default=text("false"))
    anevrizma = Column(Boolean, nullable=False, server_default=text("false"))
    note = Column(Text)
    