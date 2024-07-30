from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from shared.db.models.BASE import BaseDBModel


class AppointmentClinicalConditionBlockDBModel(BaseDBModel):
    __tablename__ = "appointment_block_clinical_conditions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, nullable=False)

    heart_failure_om = Column(Boolean)
    orthopnea = Column(Boolean)
    paroxysmal_nocturnal_dyspnea = Column(Boolean)
    reduced_exercise_tolerance = Column(Boolean)
    weakness_fatigue = Column(Boolean)
    peripheral_edema = Column(Boolean)
    ascites = Column(Boolean)
    hydrothorax = Column(Boolean)
    hydropericardium = Column(Boolean)
    night_cough = Column(Boolean)
    weight_gain_over_2kg = Column(Boolean)
    weight_loss = Column(Boolean)
    depression = Column(Boolean)
    third_heart_sound = Column(Boolean)
    apical_impulse_displacement_left = Column(Boolean)
    moist_rales_in_lungs = Column(Boolean)
    heart_murmurs = Column(Boolean)
    tachycardia = Column(Boolean)
    irregular_pulse = Column(Boolean)
    tachypnea = Column(Boolean)
    hepatomegaly = Column(Boolean)
    other_symptoms = Column(String)

    # Показатели пациента
    height = Column(Integer)  # Рост в см
    weight = Column(Float)  # Вес в кг
    bmi = Column(Float)  # ИМТ, вычисляемое
    systolic_bp = Column(Integer)  # Систолическое артериальное давление
    diastolic_bp = Column(Integer)  # Диастолическое артериальное давление
    heart_rate = Column(Integer)  # ЧСС
    six_min_walk_distance = Column(Integer)
