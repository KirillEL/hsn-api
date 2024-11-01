"""create_block_clinical_condition

Revision ID: 6525415a6f99
Revises: 72e38a033c20
Create Date: 2024-03-26 15:11:38.791239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6525415a6f99'
down_revision: Union[str, None] = '9fdc325aed89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Команды для выполнения при миграции вверх
    op.execute("""
    CREATE TABLE public.appointment_block_clinical_conditions (
        id SERIAL PRIMARY KEY,
        orthopnea BOOLEAN,
        paroxysmal_nocturnal_dyspnea BOOLEAN,
        reduced_exercise_tolerance BOOLEAN,
        weakness_fatigue BOOLEAN,
        peripheral_edema BOOLEAN,
        ascites BOOLEAN,
        hydrothorax BOOLEAN,
        hydropericardium BOOLEAN,
        night_cough BOOLEAN,
        weight_gain_over_2kg BOOLEAN,
        weight_loss BOOLEAN,
        depression BOOLEAN,
        third_heart_sound BOOLEAN,
        apical_impulse_displacement_left BOOLEAN,
        moist_rales_in_lungs BOOLEAN,
        heart_murmurs BOOLEAN,
        tachycardia BOOLEAN,
        irregular_pulse BOOLEAN,
        tachypnea BOOLEAN,
        hepatomegaly BOOLEAN,
        other_symptoms TEXT,
        height INTEGER NOT NULL,
        weight FLOAT NOT NULL,
        bmi FLOAT,
        systolic_bp INTEGER NOT NULL,
        diastolic_bp INTEGER NOT NULL,
        heart_rate INTEGER NOT NULL,
        six_min_walk_distance varchar(40),
        note text
    );
    """)

def downgrade():
    # Команды для выполнения при откате миграции
    op.execute("""
    DROP TABLE public.appointment_block_clinical_conditions;
    """)
