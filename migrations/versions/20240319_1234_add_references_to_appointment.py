"""add references to appointment

Revision ID: 3228c95a73e9
Revises: 1b1cc569bbc6
Create Date: 2024-03-19 12:34:16.178632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3228c95a73e9'
down_revision: Union[str, None] = '1b1cc569bbc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE public.patient_appointments
    ADD COLUMN appointment_complaint_id integer unique
    constraint appointment_complaint_id_fk references
    public.appointment_complaints;
    ''')

    op.execute('''
    ALTER TABLE public.patient_appointments
    ADD COLUMN appointment_laboratory_test_id integer
    unique constraint appointment_laboratory_test_id_fk references
    public.appointment_laboratory_tests;
    ''')

    op.execute('''
    ALTER TABLE public.patient_appointments
    ADD COLUMN appointment_blood_chemistry_id integer
    unique constraint appointment_blood_chemistry_id_fk references 
    public.blood_chemistries;
    ''')

    op.execute('''
    ALTER TABLE public.patient_appointments
    ADD COLUMN general_blood_analyse_id integer
    unique constraint appointment_general_blood_analyse_id_fk references 
    public.general_blood_analyses;
    ''')

    op.execute('''
    ALTER TABLE public.patient_appointments
    ADD COLUMN hormonal_blood_analyse_id integer
    unique constraint appointment_hormonal_blood_analyse_id_fk references 
    public.hormonal_blood_analyses;
    ''')

    op.execute('''
    ALTER TABLE public.patient_appointments
    ADD COLUMN general_urine_analyse_id integer
    not null unique constraint appointment_general_urine_analyse_id_fk
    references public.general_urine_analyses;
    ''')


def downgrade() -> None:
    op.execute('''
        ALTER TABLE public.patient_appointments
        DROP COLUMN appointment_complaint_id CASCADE;
        ''')

    op.execute('''
        ALTER TABLE public.patient_appointments
        DROP COLUMN appointment_laboratory_test_id CASCADE;
        ''')

    op.execute('''
        ALTER TABLE public.patient_appointments
        DROP COLUMN appointment_blood_chemistry_id CASCADE;
        ''')

    op.execute('''
        ALTER TABLE public.patient_appointments
        DROP COLUMN general_blood_analyse_id CASCADE;
        ''')

    op.execute('''
        ALTER TABLE public.patient_appointments
        DROP COLUMN hormonal_blood_analyse_id CASCADE;
        ''')

    op.execute('''
        ALTER TABLE public.patient_appointments
        DROP COLUMN general_urine_analyse_id CASCADE;
        ''')
